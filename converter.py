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
  	-d/--directory  	Base seach location
	-s/--size		File size you want to search for
	-h/--help 	Display this help and exit
    -v/--ver/--version 	Dislpays script verision

  converter.py -d /Volumes/TV Shows/ -s 1.1G

'''
from __future__ import print_function
import os, sys, getopt, logging
from os.path import expanduser

logging.basicConfig(
    format = '%(levelname)s::%(asctime)s::%(funcName)s::%(message)s',
    level = logging.DEBUG,
    filename = 'debug.log'
    )

logger = logging.getLogger(__name__)

version=1.0
ver = sys.version_info[0] > 2

org=expanduser('~/Movies/original/')
conv=expanduser('~/Movies/converted/')

directory=None
size=None
found = None

#check that the directories exist, and if not create them

class Usage(Exception):
    def __init__(self,msg):
        self.msg = msg

def usage(msg=None):
    logging.info('we hit the def usage function')
    print(__doc__)
    if msg:
        print(msg)
    return 0

def path_exists():
    logging.info('Checking Path')
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

def find_files(directory):
    logging.info('finding files')
    for folder, subfolder, filenames in os.scandir(directory):
        for name in filenames:
            if os.path.getsize(directory + name) > size:
                found.write(name)
                found.close()

def parseOptions(argv):
    logging.info('parsing options')
    global directory
    global size
    while True:
        try:
            try:
                opts,args = getopt.getopt(argv[1:],'hvd:s:',['size','version','help','directory='])
            except getopt.error as exc:
                print(exc)
                usage()
                return 0
            for o,a in opts:
                if o in ('-h','--help'):
                    usage()
                    return 0
                elif o in ('-d','--directory'):
                    directory = a
                elif o in ('-s','--size'):
                    size = a
                elif o in ('-v','--version'):
                    print('Transcoder Version: {}'.format(version))
                    return 0
                else:
                    return usage('Error: Unknown option, exiting...')
            if not directory:
                return usage('Error: Base search directory (-d/--director) not provided, exiting.')
            if not size:
                return usage('Error: File size  (-s/--size) not provided, exiting.')
        except Exception as exc:
            return usage('Error initializaing. {}'.format(str(exc)))
    return 1


def main(argv=None):
    logging.info('starting script now')
    if argv is None:
        argv = sys.argv
        init = parseOptions(argv)
        if init == 0:
            return 0
        elif init == 1:
        	return 1
    try:
        path_exists()
    except(SystemExit):
        raise

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt as exc:
        sys.exit('User cancelled, exiting.')