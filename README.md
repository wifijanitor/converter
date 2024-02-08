# Converter
Script to find video files of a specified size, or greater, and run ffmpeg to transcode them.

If you want to use other codecs, you can modify the vcodec and acodec variables with which ever codecs you have installed that work with ffmpeg
default language is english, if you want to keep a different language, you can change the `lang` variable use the three character version of ISO 639

This script does require the "humanize" python package to convert to human readable numbering

ffmpeg can be downloaded from [here](https://ffmpeg.org/download.html)

or can be installed via homebrew :
```
brew install ffmpeg 
```
current hombrew (4.x) includes x265

transcode settings are:
```
ffmpeg -i <file name> -c:v vcodec -crf 28 -map 0;a:m:language:eng-c:a acodec -b:a  bitrate -map 0:s:m:lannguaage:eng  -c:s copy output
```

This script *should* handle a file directly in the 'base' directory
or one folder level down from base

if you do not want to remove subtitles, be sure to remove the -sn from both ffmpeg lines

No kittens were harmed in the making of this script
  but my liver may be a whiner.
