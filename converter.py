#!/usr/bin/env python3

'''
Usage:

  This script will attempt to find files based on a user determined location and size.
  If the files are on a remote drive, it will copy the files to a local folder and use ffmpeg to transcode 
  and make the files smaller. The profile is will transcode up to a 1080p file using X.265 and aac encoding.

  If that completes, it will move the new file back to the original location and remove the old fiile.

  After all the files have been transcoded, it will then delete all of the files that it copied.

  Usage $program [Options]

  Input options:
  	-f/--file  	Base seach location
	-s/--size		File size you want to search for
	-h/--help 	Display this help and exit
    -v/--ver/--version 	Dislpays script verision

  converter.py -f /Volumes/TV Shows/ -s 1.1G
'''
from __future__ import print_function
import os, sys, getopt
from os.path import expanduser


version=1.0
ver = sys.version_info[0] > 2

org=expanduser('~/Movies/original/')
conv=expanduser('~/Movies/converted/')

find_file=None
size=None

#check that the directories exist, and if not create them

class Usage(Exception):
    def __init__(self,msg):
        self.msg = msg

def usage(msg=None):
    print(__doc__)
    if msg:
        print(msg)
    return 0

def path_exists():
	if not os.path.isdir(org):
		try:
			os.makedirs(org)
		except (SystemExit):
			raise
	if not os.path.isdir(conv):
		try:
			os.makedirs(conv)
		except (SystemExit):
			raise

def parseOptions(argv):
    global find_file
    global size
    while True:
        try:
            try:
                opts,args = getopt.getopt(argv[1:],'hv:f:s:',['size','ver','version','help','file='])
            except getopt.error as exc:
                return usage('Error: {}'.format(str(msg)))
            for o,a in opts:
                if o in ('-h','--help'):
                    usage()
                    return 0
                elif o in ('-f','--file'):
                    file = setFile(a)
                elif o in ('-s','--size'):
                    size=(a)
                elif o in ('-v','--ver','--version'):
                    print('Transcoder Version: {}'.format(version))
                    return 0
                else:
                    return usage('Error: Unknown option, exiting...')
            if not find_file:
                return usage('Error: Input file (-f/--file) not provided, exiting.')
            break
        except Exception as exc:
            return usage('Error initializaing. {}'.format(str(exc)))
    return 1

#def find_files

def main(argv=None):
    if argv is None:
        argv = sys.argv
        init = parseOptions(argv)
        if init == 0:
            return 0
        elif init == 1:
        	return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt as exc:
        sys.exit('User cancelled, exiting.')