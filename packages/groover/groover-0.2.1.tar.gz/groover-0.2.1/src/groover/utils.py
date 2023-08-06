import numpy as np
from numpy import linalg as la

drum_names_to_pitches = {
    "bass_drum": [35, 36],
    "closed_hihat": [42, 44],
    "crash": [49, 57],
    "floor_tom": [41, 43],
    "open_hihat": [46],
    "ride": [51, 59],
    "snare": [38, 39, 40],
    "tambourine": [54],
    "tom": [45, 47, 48, 50]
}


def add_instrument_back_pointer(midi_obj):
    for instrument in midi_obj.instruments:
        for note in instrument.notes:
            note.instrument = instrument


def pitch_weight(pitch):
    return -pitch / 128 + 1


def velocity_weight(velocity):
    return velocity / 128


def notes_weight(notes):
    pitches = np.array([note.pitch for note in notes])
    velocities = np.array([note.velocity for note in notes])

    return pitch_weight(pitches) + velocity_weight(velocities)


def cosine_similarity(a, b, epsilon=1e-8):
    a_axis = len(a.shape) - 1
    b_axis = len(b.shape) - 1
    ap = a + epsilon
    bp = b + epsilon

    return np.sum(ap * bp, axis=max(a_axis, b_axis)) / la.norm(ap, axis=a_axis) / la.norm(bp, axis=b_axis)


def rhythm_blur(a, n=3):
    axis = len(a.shape) - 1
    b = a.copy()
    for i in range(1, n):
        b += np.roll(a, i, axis=axis) * (n - i) / n
        b += np.roll(a, -i, axis=axis) * (n - i) / n

    return b


def rhythm_similarity(a, b, n=3):
    return cosine_similarity(rhythm_blur(a, n), rhythm_blur(b, n))


def get_segmented_data(pitched_dataset, drum_dataset, epsilon=5e-2, drum_similarity=cosine_similarity):
    segmented_pitches = []
    segmented_drums = []
    head = 0
    for i, (prev_drum, next_drum) in enumerate(zip(drum_dataset[:-1], drum_dataset[1:])):
        if drum_similarity(prev_drum.flatten(), next_drum.flatten()) < 1 - epsilon:
            segmented_pitches.append(pitched_dataset[head:i + 1])
            segmented_drums.append(drum_dataset[head:i + 1])
            head = i + 1

    segmented_pitches.append(pitched_dataset[head:])
    segmented_drums.append(drum_dataset[head:])

    return segmented_pitches, segmented_drums
