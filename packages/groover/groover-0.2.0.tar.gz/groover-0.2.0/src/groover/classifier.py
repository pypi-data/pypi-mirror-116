import numpy as np
from miditoolkit.midi import containers
from .utils import notes_weight as default_notes_weight
from .utils import rhythm_similarity as default_similarity
from .utils import drum_names_to_pitches, add_instrument_back_pointer
from .timepoints import get_notes_by_period


class RhythmClassifier:
    def __init__(self, bins_per_beat=24, n_beats_pitched=1, n_beats_drums=4,
                 drums=None, notes_weight=None, similarity=None):
        if drums is None:
            self.drums = ["bass_drum", "closed_hihat", "snare"]
        else:
            self.drums = drums
        self.bins_per_beat = bins_per_beat
        self.n_beats_pitched = n_beats_pitched
        self.n_beats_drums = n_beats_drums
        self.rhythms_ = dict()
        if notes_weight is None:
            self.notes_weight = default_notes_weight
        else:
            self.notes_weight = notes_weight
        if similarity is None:
            self.similarity = default_similarity
        else:
            self.similarity = similarity

    def get_heat_map(self, notes, n_bins, beat_resolution, is_drum, pitches):
        bin_resolution = np.ceil(beat_resolution / n_bins).astype(int)
        notes = [note for note in notes if note.pitch in pitches and note.instrument.is_drum == is_drum]
        heat_map = np.zeros(n_bins)
        weights = self.notes_weight(notes)
        if is_drum:
            weights = np.clip(np.ceil(weights), 0., 1.)
        for note, weight in zip(notes, weights):
            heat_map[(note.start % beat_resolution) // bin_resolution] += weight

        return heat_map

    def get_heat_maps(self, midi_obj, n_beats, is_drum, pitches=None):
        if pitches is None:
            pitches = list(range(128))

        add_instrument_back_pointer(midi_obj)
        notes = []
        for instrument in midi_obj.instruments:
            notes += instrument.notes
        notes_by_beats = get_notes_by_period(notes, resolution=midi_obj.ticks_per_beat * n_beats)

        return np.stack([
            self.get_heat_map(
                notes=note_set,
                n_bins=self.bins_per_beat * n_beats,
                beat_resolution=midi_obj.ticks_per_beat * n_beats,
                is_drum=is_drum,
                pitches=pitches
            )
            for note_set in notes_by_beats])

    def get_drum_maps(self, midi_obj, n_beats):
        return np.stack([self.get_heat_maps(
            midi_obj=midi_obj,
            n_beats=n_beats,
            is_drum=True,
            pitches=drum_names_to_pitches[drum]
        ) for drum in self.drums], axis=1)

    def get_pitched_dataset(self, midi_objs, pitches=None, in_four=False):
        if pitches is None:
            pitches = list(range(128))

        dataset = np.zeros((0, self.bins_per_beat * self.n_beats_pitched))
        for midi_obj in midi_objs:
            if in_four:
                time_signatures = midi_obj.time_signature_changes
                if len(time_signatures) > 1:
                    continue
                num = time_signatures[0].numerator
                while num % 2 == 0:
                    num /= 2
                if num != 1:
                    continue

            heat_maps = self.get_heat_maps(
                midi_obj=midi_obj,
                n_beats=self.n_beats_pitched,
                is_drum=False,
                pitches=pitches
            )
            dataset = np.concatenate((dataset, heat_maps))

        return dataset

    def get_drum_dataset(self, midi_objs, in_four=True):
        dataset = np.zeros((0, len(self.drums), self.bins_per_beat * self.n_beats_drums))
        for midi_obj in midi_objs:
            if in_four:
                time_signatures = midi_obj.time_signature_changes
                if len(time_signatures) > 1:
                    continue
                num = time_signatures[0].numerator
                while num % 2 == 0:
                    num /= 2
                if num != 1:
                    continue

            drum_maps = self.get_drum_maps(midi_obj=midi_obj, n_beats=self.n_beats_drums)
            dataset = np.concatenate((dataset, drum_maps))

        return dataset

    def fit_pitch(self, dataset, k, max_iter=1000, epsilon=1e-6):
        N, n_features = dataset.shape
        if N < k:
            raise AssertionError("Cannot have number of classes more than number of data points")
        init_indices = np.random.choice(N, size=k, replace=False)
        cluster_centers = dataset[init_indices]
        for i in range(max_iter):
            new_centers = cluster_centers.copy()
            n_points = np.ones((k, 1))

            for data in dataset:
                cluster = np.argmax(self.similarity(data, cluster_centers))
                new_centers[cluster] += data
                n_points[cluster, 0] += 1

            new_centers = new_centers / n_points

            if np.mean(self.similarity(new_centers, cluster_centers)) > 1 - epsilon:
                self.rhythms_["all_pitched"] = new_centers
                return
            else:
                cluster_centers = new_centers

        self.rhythms_["all_pitched"] = cluster_centers

    def fit_drum(self, dataset, k, drum="all_drums", quantize=True):
        dataset_temp = dataset.copy()

        if drum == "all_drums":
            indices = np.arange(dataset_temp.shape[1])
        else:
            indices = np.array([self.drums.index(drum)])

        if quantize:
            quantize_unit = self.bins_per_beat * self.n_beats_drums // 16
            for i in np.arange(16):
                dataset_temp[:, :, (i * quantize_unit + 1):((i + 1) * quantize_unit // 16)] = 0

        rhythm_count = dict()
        for data in dataset_temp[:, indices].reshape(dataset_temp.shape[0], len(indices) * dataset_temp.shape[2]):
            rhythm_tuple = tuple(data)
            if rhythm_tuple in rhythm_count.keys():
                rhythm_count[rhythm_tuple] += 1
            else:
                rhythm_count[rhythm_tuple] = 1

        pairs = sorted(list(rhythm_count.items()), key=lambda x: -x[1])
        self.rhythms_[drum] = np.array([pair[0] for pair in pairs])[:k]

    def fit_from_midi(self, midi_objs, k_pitched=200, k_all_drums=100, k_single_drum=20, quantize=True):
        pitched_dataset = self.get_pitched_dataset(midi_objs)
        self.fit_pitch(pitched_dataset, k=k_pitched)
        drum_dataset = self.get_drum_dataset(midi_objs)
        self.fit_drum(drum_dataset, k=k_all_drums, quantize=quantize)
        for drum in self.drums:
            self.fit_drum(drum_dataset, k=k_single_drum, drum=drum, quantize=quantize)

    def add_pitched_markers(self, midi_obj, pitches=None):
        if pitches is None:
            pitches = list(range(128))

        heat_maps = self.get_heat_maps(midi_obj, n_beats=self.n_beats_pitched, is_drum=False, pitches=pitches)
        for beat, heat_map in enumerate(heat_maps):
            rhythm_type = np.argmax(self.similarity(heat_map, self.rhythms_["all_pitched"]))
            marker = containers.Marker(text=f'pitched rhythm {int(rhythm_type)}',
                                       time=beat * midi_obj.ticks_per_beat * self.n_beats_pitched)
            midi_obj.markers.append(marker)

    def add_composite_drum_markers(self, midi_obj, rid_empty=True):
        drum_maps = self.get_drum_maps(midi_obj, n_beats=self.n_beats_drums)

        for bar, drum_map in enumerate(
                drum_maps.reshape(drum_maps.shape[0], len(self.drums) * self.bins_per_beat * self.n_beats_drums)):
            rhythm_type = np.argmax(self.similarity(drum_map, self.rhythms_["all_drums"]))
            if rid_empty:
                if np.sum(self.rhythms_["all_drums"][rhythm_type]) == 0.:
                    continue
            marker = containers.Marker(text=f'drums rhythm {int(rhythm_type)}',
                                       time=bar * midi_obj.ticks_per_beat * self.n_beats_drums)
            midi_obj.markers.append(marker)

    def add_separate_drum_markers(self, midi_obj, rid_empty=True):
        drum_maps = self.get_drum_maps(midi_obj, n_beats=self.n_beats_drums)

        for i_drum, drum in enumerate(self.drums):
            for bar, drum_map in enumerate(
                    drum_maps[:, i_drum, :].reshape(drum_maps.shape[0], self.bins_per_beat * self.n_beats_drums)):
                rhythm_type = np.argmax(self.similarity(drum_map, self.rhythms_[drum]))
                if rid_empty:
                    if np.sum(self.rhythms_[drum][rhythm_type]) == 0.:
                        continue
                marker = containers.Marker(text=f'{drum} rhythm {int(rhythm_type)}',
                                           time=bar * midi_obj.ticks_per_beat * self.n_beats_drums)
                midi_obj.markers.append(marker)
