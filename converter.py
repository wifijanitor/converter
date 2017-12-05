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

import os, sys, getopt, humanize, glob, logging
from pathlib import Path
from os.path import expanduser


logging.basicConfig(
    format = '%(levelname)s::%(asctime)s::%(funcName)s::%(message)s',
    level = logging.DEBUG,
    )

logger = logging.getLogger(__name__)

version = 1.0
ver = sys.version_info[0] > 2

directory = None
size = None

org = expanduser('~/Converter/original/')
conv = expanduser('~/Converter/modified/')
found = expanduser('~/Converter/found.txt')


class Usage(Exception):
    def __init__(self,msg):
        self.msg = msg

def usage(msg=None):
    logging.info('we hit the def usage function')
    print(__doc__)
    if msg:
        print(msg)

def parseOptions(argv):
    global directory
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
                    directory = str(a)
                elif o in ('-s','--size'):
                    if not directory:
                        return usage('Error: Base search directory (-d/--directory) not provided, exiting.')
                        if not size:
                            return usage('Error: File size  (-s/--size) not provided, exiting.')
        except Exception as exc:
            return usage('Error:{}'.format(str(exc)))
        return 1

def path_exists():
    try:
        if not os.path.isdir(org):
            os.makedirs(org)
        if not os.path.isdir(conv):
            os.makedirs(conv)
    except Exception as esc:
        print('Error {}'.format(str(esc)))
        return
    return 1

def find_files():
    logging.info('finding files')
    os.chdir(directory)
    with open(found, 'w') as files:
        logging.info(directory)
        for f in glob.glob('**/*.mkv'):
            files.write(f + '\n')



#def clean_up():



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