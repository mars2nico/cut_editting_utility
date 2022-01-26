#!/bin/bash
ffmpeg -loglevel quiet -f lavfi -i smptehdbars -f lavfi -i sine=1000 -to 0:0:15 -filter_complex_script fvad_script.txt -f null - && diff result/fvad_expect.txt result/fvad_result.txt
