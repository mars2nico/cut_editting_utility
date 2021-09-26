# Cut Editing Utility

# Install Prerquisite
- git
- python
- [forked libfvad](https://github.com/mars2nico/libfvad) (from source)
- FFmpeg (from source)

# Dependency modules
- FFmpeg Filters
  * Audio
    - aformat
    - astats
    - ametadata
    - dcshift
    - agate
    - silencedetect
    - fvad (Indicated at following section.)

# Quick Start
- Clone repository or download and extract this repository's Zip file.
- Move into libfvad source code directory.
- Build and install libfvad.
- Move into FFmpeg source code directory.
- Add the audio filter 'af_fvad' to FFmpeg source.

```console
    git apply /path/to/cut_editting_utility/libavfilter_add_af_libfvad.patch
```

- Build and install FFmpeg.
- Move into the cut editting utility directry.
- Run the script.

  Note: This project does not contains sample data.
- The script outputs 'metadata.txt'.
