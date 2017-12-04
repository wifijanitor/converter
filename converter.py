#!/usr/bin/env python3

'''
Usage:
  This script will attempt to find files based on a user determined location and size.
  If the files are on a remote drive, it will copy the files to a local folder and use ffmpeg to transcode 
  and make the files smaller. The profile is will transcode up to a 1080p file using X.265 and aac encoding.
  If that completes, it will move the new file back to the original location and remove the old fiile.
  After all the files have been transcoded, it will then delete all of the files that it copied.
  
  Input options:
    
    -d/--directory      Base seach location
    -s/--size           File size you want to search for
    -h/--help           Display this help and exit
    -v/--ver/--version  Dislpays script verision

  converter.py -d /Volumes/TV Shows/ -s 1.6G
'''

import os, sys, getopt, logging
from os.path import expanduser
from time import sleep

logging.basicConfig(
    format = '%(levelname)s::%(asctime)s::%(funcName)s::%(message)s',
    level = logging.DEBUG,
    filename = 'debug.log'
    )

logger = logging.getLogger(__name__)

version = 1.0
ver = sys.version_info[0] > 2

org = expanduser('~/Movies/original/')
conv = expanduser('~/Movies/converted/')
found = open(expanduser('~/Movies/') + 'found.txt', 'w')

path = None
size = None

#check that the directories exist, and if not create them

class Usage(Exception):
    def __init__(self,msg):
        self.msg = msg

def usage(msg=None):
    logging.info('we hit the def usage function')
    print(__doc__)
    if msg:
        print(msg)

def path_exists():
    logging.info('Checking Path')
    try:
        if not os.path.isdir(org):
            os.makedirs(org)
        elif not os.path.isdir(conv):
            os.makedirs(conv)
    except Exception as esc:
        print('Error {}'.format(str(esc)))
        return
    return 1


def find_files(f):
    logging.info('finding files')
    with os.scandir(f) as directory:
        print(f)
        for folder, subfolder, filenames in directory:
            print(folder)
            print(subfolder)
            print(filenames)
            for subfolder in directory:
                for filenames in subfolder:
                    if os.path.getsize(path + name) > size:
                        files.write(name)
                        files.close()


def parseOptions(argv):
    global path
    global size
    while True:
        try:
            try:
                opts,args = getopt.getopt(argv[1:],'hvd:s:',['size=','version','help','directory='])
            except getopt.error as exc:
                return usage('Error: {}'.format(str(exc)))
            for o,a in opts:
                if o in ('-h','--help'):
                    usage()
                    return 0
                elif o in ('-v','--version'):
                    return usage('Transcoder Version: {}'.format(version))
                elif o in ('-d','--directory'):
                    logging.info('Directory found')
                    path = find_files(a + '/')
                elif o in ('-s','--size'):
                    size = a
                    logging.info('Size Found')
                else:
                    return usage('Error: Unknown option, exiting...')
            if not path:
                return usage('Error: Base search directory (-d/--director) not provided, exiting.')
            if not size:
                return usage('Error: File size  (-s/--size) not provided, exiting.')
        except Exception as exc:
            return usage('Error:{}'.format(str(exc)))
        return 1

def main(argv=None):
    if len(sys.argv) <= 1:
        return usage('No options were provided, plrease refer to usage')
    if argv is None:
        argv = sys.argv
        init = parseOptions(argv)
        logging.info(init)
        if init == 0:
            return 0
        elif init == 1:
                path_exists()
                find_files()



if __name__ == '__main__':
    try:
        sys.exit(main())
        print('Exiting')
    except KeyboardInterrupt as exc:
        sys.exit('User cancelled, exiting.')