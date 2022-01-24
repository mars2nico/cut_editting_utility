import click
import ffmpeg
import io
import subprocess
import sys
from os import path
from subprocess import PIPE

get_default_metapath = lambda x: "{0}_metadata.txt".format(path.splitext(x)[0])

def get_stats_audio(input_file):
    # ffmpeg -i $input_file -af aformat=channel_layouts=FC,astats=metadata=1:measure_perchannel=none,ametadata=mode=print:file=metadata_astats.txt -f null -
    out, err = (
        ffmpeg.input(input_file).audio
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

def proc_audio(input_file, dc_offset = 0.):
    # ffmpeg -i $input_file -af aformat=channel_layouts=FC,dcshift=shift=$dc_offset,agate,silencedetect=noise=0.1,fvad,ametadata=mode=print:file=metadata.txt -f null -
    out, err = (
        ffmpeg.input(input_file).audio
        .filter('aformat', channel_layouts="FC")
        .filter('dcshift', shift="{0:f}".format(-dc_offset))
        # .filter('agate')
        .filter('silencedetect', noise=0.1)
        .filter('fvad')
        .filter(
            'ametadata',
            mode="print",
            file=get_default_metapath(input_file)
        )
        .output('/dev/null', format="wav")
        .run(overwrite_output=True)
    )
    proc = subprocess.run("cat metadata.txt | grep -E \"^lavfi\\.(s|fvad\\.s)\"", shell=True, stdout=PIPE, stderr=PIPE, text=True)
    f = io.StringIO(proc.stdout)
    for line in f:
        items = line.rstrip("\n").split("=", maxsplit=1)
        print("{0:40}:{1}".format(items[0], items[1]))
    return

@click.group()
def group():
    pass

@group.command()
@click.argument('input_file', type=click.Path(exists=True))
def scanvideo(input_file):
    dc_offset = get_stats_audio(input_file)
    proc_audio(input_file, dc_offset)

def main():
    group()

if __name__ == '__main__':
    main()
