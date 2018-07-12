#!/usr/bin/env python3

'''
Usage:
  This script will attempt to find files based on
  user determined location and size.

  Currently this only works for MP4 and MKV extensions, I'll add in
  AVI functionality at some point.

  If the files are on a remote drive, it will copy the files
  to a local folder and use ffmpeg to transcode and make the files smaller.

  The profile is will transcode up to a 1080p file
  using X.265 and aac encoding.

  If that completes, it will:
  remove the old fiile
  move the new file back to the original location.

  Input options:

    -d/--directory      Base seach location
    -s/--size           File size you want to search for G assumed
    -h/--help           Display this help and exit
    -v/--ver/--version  Dislpays script verision

  converter.py -d /Volumes/TV Shows/ -s 11
'''

import os
import sys
import getopt
import glob
import subprocess
import shutil
import logging
from os.path import expanduser


logging.basicConfig(
    format='%(asctime)s--%(funcName)s--%(levelname)s--%(message)s',
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)

version = 2.0
ver = sys.version_info[0] > 2

directory = None
size = None
bsize = None

org = expanduser('~/Converter/original/')
conv = expanduser('~/Converter/modified/')
found = expanduser('~/Converter/found.txt')


class Usage(Exception):
    def __init__(self, msg):
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
                opts, args = getopt.getopt(
                    argv[1:], 'hvd:s:', ['size=', 'version', 'help', 'directory='])
            except getopt.error as exc:
                return usage('Error: {}'.format(str(exc)))
            for o, a in opts:
                if o in ('-h', '--help'):
                    usage()
                    return 0
                elif o in ('-v', '--version'):
                    return usage('Transcoder Version: {}'.format(version))
                elif o in ('-d', '--directory'):
                    directory = str(a)
                elif o in ('-s', '--size'):
                    size = int(a) << 30
                else:
                    return usage('Error: Unknown option, exiting...')
            if not directory:
                return usage('Error: Base search directory \
                    (-d/--directory) not provided, exiting.')
            if not size:
                return usage('Error: File size \
                    (-s/--size) not provided, exiting.')
        except Exception as exc:
            return usage('Error:{}'.format(str(exc)))
        return 1


def path_exists():
    '''
    checks if the path to the folder structure exists.
    if not, it will create it
    '''
    try:
        if not os.path.isdir(org):
            logging.info('creating' + str(org))
            os.makedirs(org)
        if not os.path.isdir(conv):
            logging.info('creating' + str(conv))
            os.makedirs(conv)
    except Exception as esc:
        print('Error {}'.format(str(esc)))
        return


def find_files():
    '''
    attempts to find files of the specified size in the specified directory
    writes names to a text file for future reference
    '''
    os.chdir(directory)
    with open(found, 'wt') as file:
        logging.info('Finding files')
        for f in glob.iglob('**/*.m*', recursive=True):
            file_size = os.path.getsize(f)
            if file_size >= size:
                file.write(f + '\n')
            else:
                continue


def convert():
    '''
    converts files to X265 video and AAC audio codecs
    '''
    os.chdir(org)
    logging.info("Starting to convert ")
    with open(found, 'rt') as shows:
        for row in shows:
            line = row.rstrip().split('/')
            print('This is the file we are moving')
            if 'mkv' in line[0] or 'mp4' in line[0]:
                file = line[0]
                logging.info('Moving ' + file + ' for conversion')
                shutil.move(directory + '/' + file, org)
                logging.info('Converting ' + file)
                subprocess.run(
                    'ffmpeg -sn -i ' + '"' + file + '"' +
                    ' -c:v libx265 -crf 28 -c:a aac -b:a  128k ' +
                    conv + '"' + file + '"' + ' -hide_banner', shell=True
                )
                logging.info('Done converting' + line[0])
            elif 'mkv' in line[1] or 'mp4' in line[1]:
                file = line[1]
                folder = line[0]
                logging.info('Moving ' + file + ' for conversion')
                shutil.move(directory + '/' + folder + '/' + file, org)
                logging.info('Converting ' + file)
                subprocess.run(
                    'ffmpeg -sn -i ' + '"' + file + '"' +
                    ' -c:v libx265 -crf 28 -c:a aac -b:a 128k ' +
                    conv + '"' + file + '"' + ' -hide_banner', shell=True
                )


def move_conv():
    '''
    moves newly converted media back to it's original location
    changes file extension from mp4 to mkv.
    '''
    os.chdir(conv)
    with open(found, 'rt') as file:
        for row in file:
            line = row.rstrip().split('/')
            if 'mkv' in line[0]:
                file = line[0]
                logging.info('Moving ' + file +
                             " back to it's original location")
                shutil.move(file, directory + '/' + file)
            elif 'mp4' in line[0]:
                file = line[0]
                logging.info('Moving ' + file +
                             " back to it's original location")
                shutil.move(file, directory + '/' +
                            os.path.splitext(file)[0] + '.mkv')
            elif 'mkv' in line[1]:
                file = line[1]
                folder = line[0]
                logging.info('Moving ' + file +
                             " back to it's orignial location")
                shutil.move(file, directory + '/' +
                            folder + '/' + file)
            elif 'mp4' in line[1]:
                file = line[1]
                folder = line[0]
                logging.info('Moving ' + file +
                             " back to it's orignial location")
                shutil.move(file, directory + '/' +
                            folder + '/' + os.path.splitext(file)[0] + '.mkv')


def clean_up():
    ''' 
    cleans out the temporary storage directory
    '''
    os.chdir(org)
    logging.info("Cleaning up")
    with open(found, 'rt') as shows:
        for row in shows:
            line = row.rstrip()
            os.remove(line)


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
            convert()
            move_conv()
            clean_up()


if __name__ == '__main__':
    try:
        sys.exit(main())
        print('Exiting')
    except KeyboardInterrupt as exc:
        sys.exit('User cancelled, exiting.')
