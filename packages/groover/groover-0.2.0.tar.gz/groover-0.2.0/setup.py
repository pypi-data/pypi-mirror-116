import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="groover",
    version="0.2.0",
    author="Joshua Chang",
    author_email="chchang6@illinois.edu",
    description="A rhythm feature extractor and classifier for MIDI files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/joshuachang2311/chorder",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "miditoolkit"
    ]
)
