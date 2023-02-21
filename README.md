# Converter
Script to find video files of a specified size, or greater, and run ffmpeg to transcode them.

If you want to use other codecs, you can modify the vcodec and acodec variables with which ever codecs you have installed that work with ffmpeg

ffmpeg can be downloaded from [here](https://ffmpeg.org/download.html)

or can be installed via homebrew :
```
brew install ffmpeg 
```
current hombrew (4.x) includes x265

transcode settings are:
```
ffmpeg -i <file name> -c:v vcodec -crf crf -c:a acodec -b:a  bitrate output
```

This script *should* handle a file directly in the 'base' directory
or one folder level down from base

if you do not want to remove subtitles, be sure to remove the -sn from both ffmpeg lines

No kittens were harmed in the making of this script
  but my liver may be a whiner.