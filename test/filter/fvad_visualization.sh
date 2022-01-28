#!/bin/bash

pushd fvad_visualization

ffmpeg -f lavfi -i ${1:-smptehdbars} -f lavfi -i ${2:-sine=1000} -to 0:0:15 -filter_complex_script sample.txt -map [out0] -map 1:a -f matroska - | ffplay -i -

popd

# Example
# 1) Exec by test source
# $ ./fvad_visualization.sh
#
# 2) Exec with a file
# $ ./fvad_visualization.sh movie=`realpath ../data/in.mp4` amovie=`realpath ../data/in.mp4`
#
# Note: Absolute path required
