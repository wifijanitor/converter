#!/usr/bin/env python3

'''
Usage:
  This script will attempt to find files based on
  user determined location and size.

  If the files are on a remote drive, it will copy the files
  to a local folder and use ffmpeg to transcode and make the files smaller.

  The profile is will transcode up to a 1080p file
  using X.265 and aac encoding.

  If that completes, it will:
  remove the old fiile
  move the new file back to the original location.

  Input options:

    -d/--directory      Base seach location
    -s/--size           File size you want to search for
    -h/--help           Display this help and exit
    -v/--ver/--version  Dislpays script verision

  converter.py -d /Volumes/TV Shows/ -s 1.6G
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

version = 1.0
ver = sys.version_info[0] > 2

directory = None
size = None

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
                    size = a
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
    return 1


def find_files():
    os.chdir(directory)
    with open(found, 'wt') as file:
        logging.info('Finding files')
        for f in glob.iglob('**/*.m*', recursive=True):
            file.write(f + '\n')


def convert():
    os.chdir(org)
    print('This is where we are')
    print(os.getcwd())
    logging.info("Starting to convert ")
    with open(found, 'rt') as shows:
        for line in shows:
            line = line.rstrip().split('/')
            print('This is the file we are moving')
            print(line)
            if len(line) < 1:
                logging.info('Moving ' + line[1] + ' for conversion')
                shutil.move(directory + '/' + line[0] + '/' + line[1], org)
                logging.info('Converting ' + line[1])
                subprocess.run(
                    'ffmpeg -sn -i ' + '"' + line[1] + '"' +
                    ' -cv libx265 -crf 28 -c:a aac -b:a 128k ' +
                    conv + '"' + line[1] + '"' + ' -hide_banner', shell=True
                )
            else:
                logging.info('Moving ' + line[0] + ' for conversion')
                shutil.move(directory + '/' + line[0], org)
                logging.info('Converting ' + line[0])
                subprocess.run(
                    'ffmpeg -sn -i ' + '"' + line[0] + '"' +
                    ' -c:v libx265 -crf 28 -c:a aac -b:a  128k ' +
                    conv + '"' + line[0] + '"' + ' -hide_banner', shell=True
                )


def move_conv():
    os.chdir(conv)
    with open(found, 'rt') as file:
        for line in file:
            line = line.rstrip().split('/')
            if line[1] is None:
                logging.info('Moving ' + line[0] +
                             " back to it's orignial location")
                shutil.move(line[0], directory + '/' + line[0])
            else:
                logging.info('Moving' + line[1] +
                             " back to it's original location")
                shutil.move(line[1], directory + '/' + line[0] + '/' + line[1])


def clean_up():
    os.chdir(org)
    logging.info("Cleaning up")
    with open(found, 'rt') as shows:
        for line in shows:
            line = line.rstrip().split('/')
            if line[1] is None:
                os.remove(line[0])
            else:
                os.remove(line[1])


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
            # clean_up()


if __name__ == '__main__':
    try:
        sys.exit(main())
        print('Exiting')
    except KeyboardInterrupt as exc:
        sys.exit('User cancelled, exiting.')
