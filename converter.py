#!/usr/bin/env python3

import os
import argparse
import glob
import subprocess
import shutil
import logging
import sys
import humanize
from os.path import expanduser


logging.basicConfig(
    format='%(asctime)s--%(funcName)s--%(levelname)s--%(message)s',
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)

directory = None
size = None
vcodec = 'libx265'
acodec = 'aac'
crf = '28'
lang = 'eng'
bitrate = '128k'

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
                        version='%(prog)s 4.4')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    directory = str(args.directory)
    size = (args.size) * 1024**3


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
        logging.info(
            f'Searching for files in {directory}'
            f' over {humanize.naturalsize(size, gnu=True)}')
        for f in glob.iglob('**/*.[a,f,m,w]*', recursive=True):
            file_size = os.path.getsize(f)
            if file_size >= size:
                logging.info(
                    f'Found  {f} is '
                    f'{humanize.naturalsize(file_size, gnu=True)}')
                file.write(f + '\n')
            else:
                continue


def move_org():
    with open(found, 'rt') as shows:
        for row in shows:
            file = row.rstrip().split('/')
            if len(file) == 1:
                name = file[0]
                movie = name[:-4]
                data = {'name': name, 'movie': movie}
                logging.info(f'Moving {movie} for conversion')
                shutil.move(directory + '/' + name, org)
                convert_file(**data)
                move_conv(**data)
                clean_up(**data)
            else:
                folder = file[0]
                name = file[1]
                movie = name[:-4]
                data = {'folder': folder, 'name': name, 'movie': movie}
                logging.info(f'Moving {movie} for conversion')
                shutil.move(directory + '/' + folder + '/' + name, org)
                convert_file(**data)
                move_conv(**data)
                clean_up(**data)


def convert_file(**kwargs):
    name = kwargs.get('name')
    movie = kwargs.get('movie')
    '''
    converts files to X265 video and AAC audio codecs
    '''
    os.chdir(org)
    logging.info(f'Converting {movie}')
    print(name, movie)
    subprocess.run(
        'ffmpeg -sn -i ' + '"' + name + '"'
        + ' -map 0:v:0'
        + ' -c:v ' + vcodec
        + ' -crf ' + crf
        + ' -c:a ' + acodec
        + ' -map 0:a:m:language:' + lang
        + ' -b:a ' + bitrate + ' '
        + conv + '"' + movie + '.mkv' + '"' + ' -hide_banner',
        shell=True)
    logging.info(f'Done converting {movie}')


def move_conv(**kwargs):
    folder = kwargs.get('folder', '')
    movie = kwargs.get('movie')
    '''
    moves newly converted media back to it's original location
    changes file extension from mp4/avi etc to mkv.
    '''
    os.chdir(conv)
    if len(folder) >= 1:
        logging.info(f"Moving {movie} back to it's original location")
        shutil.move(movie + '.mkv', directory + '/' + folder)
    else:
        logging.info(f"Moving {movie} back to it's original location")
        shutil.move(movie + '.mkv', directory)


def clean_up(**kwargs):
    '''
    cleans out the temporary storage directory
    '''
    folder = kwargs.get('folder', '')
    name = kwargs.get('name')
    movie = kwargs.get('movie')
    os.chdir(org)
    logging.info(f"Removing the origianl version of {movie}")
    if len(folder) >= 1:
        os.remove(folder + name)
    else:
        os.remove(name)


def main():
    parseOptions()
    path_exists()
    find_files()
#    move_org()


if __name__ == '__main__':
    main()
