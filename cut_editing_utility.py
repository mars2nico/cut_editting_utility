import ffmpeg

def proc_audio():
    audio_stream = ffmpeg.input('./testdata.mkv').audio.filter('volumedetect')
    out, err = (
        audio_stream.output('/dev/null', format='wav')
        .run()
    )
    return out

proc_audio()
