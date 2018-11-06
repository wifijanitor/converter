#!/usr/bin/env python3

import os
import argparse
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

directory = None
size = None
vcodec = 'libx265'
acodec = 'libfdk_aac'
crf = '28'
bitrate = '128k'
extension = ['mkv', 'mp4', 'm4v', 'avi', 'wmv']

org = expanduser('~/Converter/original/')
conv = expanduser('~/Converter/modified/')
found = expanduser('~/Converter/found.txt')


def parseOptions():
    global directory
    global size
    parser = argparse.ArgumentParser(
        prog='Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''
            Convert files to MKV using X265 and AAC encodings, by default.
            You can use different codecs by changing the vcodec and acodec
            variables.
            "-s" matches file size greater than input, in Gigabit.
  ''')
    parser.add_argument('-d', '--directory',
                        metavar='Directory',
                        help="Base search location",
                        required=True)
    parser.add_argument('-s', '--size',
                        metavar='Size',
                        help="file size you want to search for in Gigabit",
                        type=int, required=True)
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s 3.1')
    args = parser.parse_args()
    directory = str(args.directory)
    size = ((args.size) * 1024**3)


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
        for f in glob.iglob('**/*.[a,m,w]*', recursive=True):
            file_size = os.path.getsize(f)
            if file_size >= size:
                file.write(f + '\n')
            else:
                continue


def convert_main():
    '''
    converts files to X265 video and AAC audio codecs
    '''
    os.chdir(org)
    logging.info("Starting to convert ")
    with open(found, 'rt') as shows:
        for row in shows:
            file = row.rstrip().split('/')
            if len(file) == 1:
                print(file[0])
                movie, ext = file[0].split('.')
                if any(ext for ext in extension):
                    logging.info(f'Moving {movie} for conversion')
                    shutil.move(directory + '/' + file[0], org)
                    logging.info(f'Converting {movie}')
                    subprocess.run(
                        'ffmpeg -sn -i ' + '"' + file[0] + '"' +
                        ' -c:v ' + vcodec +
                        ' -crf ' + crf +
                        ' -c:a ' + acodec +
                        ' -b:a ' + bitrate + ' ' +
                        conv + '"' + movie + '.mkv' + '"' + ' -hide_banner',
                        shell=True)
                    logging.info(f'Done converting {movie}')
            else:
                print(file[0])
                print(file[1])
                movie, ext = file[1].split('.')
                shutil.move(directory + '/' + file[0] + '/' + file[1], org)
                logging.info(f'Converting {movie}')
                subprocess.run(
                    'ffmpeg -sn -i ' + '"' + file[1] + '"' +
                    ' -c:v ' + vcodec +
                    ' -crf ' + crf +
                    ' -c:a ' + acodec +
                    ' -b:a ' + bitrate + ' ' +
                    conv + '"' + movie + '.mkv' + '"' + ' -hide_banner',
                    shell=True)
                logging.info(f'Done converting {movie}')


def move_conv():
    '''
    moves newly converted media back to it's original location
    changes file extension from mp4 to mkv.
    '''
    os.chdir(conv)
    with open(found, 'rt') as shows:
        for row in shows:
            file = row.rstrip().split('/')
            if len(file) == 1:
                print(file[0])
                movie, ext = file[0].split('.')
                if any(ext for ext in extension):
                    logging.info(
                        f"Moving {movie} back to it's original location")
                    shutil.move(movie + '.mkv', directory)
            else:
                movie, ext = file[1].split('.')
                logging.info(f"Moving {movie} back to it's original location")
                shutil.move(movie + '.mkv', directory + '/' + file[0])


def clean_up():
    '''
    cleans out the temporary storage directory
    '''
    os.chdir(org)
    logging.info("Cleaning up")
    with open(found, 'rt') as shows:
        for row in shows:
            *junk, line = row.rstrip().split('/')
            os.remove(line)


def main():
    parseOptions()
    path_exists()
    find_files()
    convert_main()
    move_conv()
    clean_up()


if __name__ == '__main__':
    main()
