import ffmpeg
import subprocess
import io
from subprocess import PIPE

def get_stats_audio():
    # ffmpeg -i testdata.mkv -af aformat=channel_layouts=FC,astats=metadata=1:measure_perchannel=none,ametadata=mode=print:file=metadata_astats.txt -f null -
    out, err = (
        ffmpeg.input('./testdata.mkv').audio
        .filter('aformat', channel_layouts="FC")
        .filter('astats', metadata=1, measure_perchannel="none")
        .filter('ametadata', mode="print", file="metadata_astats.txt")
        .output('/dev/null', format="wav")
        .run(overwrite_output=True)
    )
    proc = subprocess.run("cat metadata_astats.txt | grep lavfi.astats.Overall.DC_offset", shell=True, stdout=PIPE, stderr=PIPE, text=True)
    f = io.StringIO(proc.stdout)
    sum = 0.
    cnt = 0
    for line in f:
        sum += float(line.split("=")[1])
        cnt += 1
    return sum / cnt

def proc_audio(dc_offset = 0.):
    # ffmpeg -i testdata.mkv -af aformat=channel_layouts=FC,dcshift=shift=$dc_offset,agate,silencedetect=noise=0.1,ametadata=mode=print:file=metadata.txt -f null -
    out, err = (
        ffmpeg.input('./testdata.mkv').audio
        .filter('aformat', channel_layouts="FC")
        .filter('dcshift', shift="{0:f}".format(-dc_offset))
        .filter('agate')
        .filter('silencedetect', noise=0.1)
        .filter('fvad')
        .filter('ametadata', mode="print", file="metadata.txt")
        .output('/dev/null', format="wav")
        .run(overwrite_output=True)
    )
    proc = subprocess.run("cat metadata.txt | grep lavfi", shell=True, stdout=PIPE, stderr=PIPE, text=True)
    f = io.StringIO(proc.stdout)
    for line in f:
        items = line.rstrip("\n").split("=")
        print("{0:40}:{1}".format(items[0], items[1]))
    return

dc_offset = get_stats_audio()
proc_audio(dc_offset)
