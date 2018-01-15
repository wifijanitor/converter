# Converter
Script to find Move/TV show files of a specified size and run ffmpeg to transcode to a smaller file size.

**AND REMOVE SUBTITLES**

ffmpeg must be installed, with the libx265 for this to work.
this can be downloaded from [here](https://ffmpeg.org/download.html)

transcode settings are:
```
ffmpeg -sn <file name> -c:v libx265 -crf 28 -c:a aac -b:a  128k output
```

This script *should* handle a file directly in the 'base' directory
or one folder level down from base

if you do not want to remove subtitles, be sure to remove the -sn from both ffmpeg lines