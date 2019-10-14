# Converter
Script to find video files of a specified size, or greater, and run ffmpeg to transcode them.

Currently keeps english language subtitles you can change this using the ISO 639-2 code

If you want to use other codecs, you can modify the vcodec and acodec variables with which ever codecs you have installed that work with ffmpeg

ffmpeg can be downloaded from [here](https://ffmpeg.org/download.html)

or can be installed via homebrew :
```
brew install ffmpeg
```

## Options

Variable | Default | Description
-------------|-------------|------------------
vcodec | libx265 | video codec
acodec | aac | audio codec
subs | eng | ISO 639-2 code

This script *should* handle a file directly in the 'base' directory
or one folder level down from base


No kittens were harmed in the making of this script
  but my liver may be a whiner.