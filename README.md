
Script to find Move/TV show files of a specified size and run ffmpeg to transcode to a smaller file size.

ffmpeg must be installed for this to work.
transcode settings are:
-c:v libx265 -crf 28 -c:a aac -b:a  128k

call the script raw to get usage.