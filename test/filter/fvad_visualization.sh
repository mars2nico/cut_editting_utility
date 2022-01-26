#!/bin/bash

pushd fvad_visualization

ffmpeg ${1:--f lavfi -i smptehdbars} ${2:--f lavfi -i sine=1000} -to 0:0:15 -filter_complex_script sample.txt -map [out0] -map 1:a -f matroska - | ffplay -i -

popd
