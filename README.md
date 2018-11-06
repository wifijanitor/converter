# Converter
Script to find video files of a specified size, or greater, and run ffmpeg to transcode them.

**AND REMOVE SUBTITLES**

ffmpeg must be installed, with the libx265 and libfdk_aac for this to work by default.

If you want to use other codecs, you can modify the vcodec and acodec variables with which ever codecs you have installed that work with ffmpeg

ffmpeg can be downloaded from [here](https://ffmpeg.org/download.html)

or can be installed via homebrew :
```
ffmpeg --with-fdk-aac  --with-x265
```

transcode settings are:
```
ffmpeg -sn <file name> -c:v vcodec -crf crf -c:a acodec -b:a  bitrate output
```

This script *should* handle a file directly in the 'base' directory
or one folder level down from base

if you do not want to remove subtitles, be sure to remove the -sn from both ffmpeg lines

No kittens were harmed in the making of this script
  but my liver may be a whiner.