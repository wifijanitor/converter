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
            Convert files to MKV using X265 and AAC encodings
  ''')
    parser.add_argument('-d', '--directory',
                        metavar='Directory',
                        help="Base search location",
                        required=True)
    parser.add_argument('-s', '--size',
                        metavar='Size',
                        help="file size you want to search for",
                        type=int, required=True)
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s 3.0')
    args = parser.parse_args()
    directory = str(args.directory)
    size = args.size


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
        for f in glob.iglob('**/*.**', recursive=True):
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
            movie, ext = row.rstrip().split('.')
            if 'mkv' in ext:
                convert_mkv(row)
            elif 'mp4' in ext:
                convert_mp4(row)
            elif 'avi' in ext:
                convert_avi(row)


def convert_mkv(row):
    line = row.rstrip().split('/')
    if 'mkv' in line[0]:
        file = line[0]
        print(f'Converting {file}')
        logging.info(f'Moving {file} for conversion')
        shutil.move(directory + '/' + file, org)
        logging.info(f'Converting {file}')
        subprocess.run(
            'ffmpeg -sn -i ' + '"' + file + '"' +
            ' -c:v libx265 -crf 28 -c:a libfdk_aac -b:a  128k ' +
            conv + '"' + file + '"' + ' -hide_banner', shell=True
        )
        logging.info(f'Done converting {file}')
    elif 'mkv' in line[1]:
        file = line[1]
        folder = line[0]
        logging.info(f'Moving {file} for conversion')
        shutil.move(directory + '/' + folder + '/' + file, org)
        logging.info(f'Converting {file}')
        subprocess.run(
            'ffmpeg -sn -i ' + '"' + file + '"' +
            ' -c:v libx265 -crf 28 -c:a aac -b:a 128k ' +
            conv + '"' + file + '"' + ' -hide_banner', shell=True
        )
    return


def convert_mp4(row):
    line = row.rstrip().split('/')
    if 'mp4' in line[0]:
        old, ext = line[0].split('.')
        file = line[0]
        logging.info(f'Moving {file} for conversion')
        shutil.move(directory + '/' + file, org)
        logging.info(f'Converting {file}')
        subprocess.run(
            'ffmpeg -sn -i ' + '"' + file + '"' +
            ' -c:v libx265 -crf 28 -c:a libfdk_aac -b:a  128k ' +
            conv + '"' + old + '.mkv' + '"' + ' -hide_banner',
            shell=True)
        logging.info(f'Done converting {file}')
    elif 'mp4' in line[1]:
        old, ext = line[1].split('.')
        file = line[1]
        folder = line[0]
        shutil.move(directory + '/' + folder + '/' + file, org)
        logging.info(f'Converting {file}')
        subprocess.run(
            'ffmpeg -sn -i ' + '"' + file + '"' +
            ' -c:v libx265 -crf 28 -c:a libfdk_aac -b:a  128k ' +
            conv + '"' + old + '.mkv' + '"' + ' -hide_banner',
            shell=True)
    return


def convert_avi(row):
    line = row.rstrip().split('/')
    if 'avi' in line[0]:
        old, ext = line[0].split('.')
        file = line[0]
        logging.info(f'Moving {file} for conversion')
        shutil.move(directory + '/' + file, org)
        logging.info(f'Converting {file}')
        subprocess.run(
            'ffmpeg -sn -i ' + '"' + file + '"' +
            ' -c:v libx265 -crf 28 -c:a libfdk_aac -b:a  128k ' +
            conv + '"' + old + '.mkv' + '"' + ' -hide_banner',
            shell=True)
        logging.info(f'Done converting {file}')
    elif 'avi' in line[1]:
        old, ext = line[1].split('.')
        file = line[1]
        folder = line[0]
        shutil.move(directory + '/' + folder + '/' + file, org)
        logging.info(f'Converting {file}')
        subprocess.run(
            'ffmpeg -sn -i ' + '"' + file + '"' +
            ' -c:v libx265 -crf 28 -c:a libfdk_aac -b:a  128k ' +
            conv + '"' + old + '.mkv' + '"' + ' -hide_banner',
            shell=True)
    return


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
                logging.info(f"Moving {file} back to it's original location")
                shutil.move(file, directory)
            elif 'mp4' in line[0]:
                old, ext = line[0].split('.')
                file = line[0]
                logging.info(f"Moving {file} back to it's original location")
                shutil.move(old + ".mkv", directory)
            elif 'avi' in line[0]:
                old, ext = line[0].split('.')
                file = line[0]
                logging.info(f"Moving {file} back to it's original location")
                shutil.move(old + ".mkv", directory)
            elif 'mkv' in line[1]:
                file = line[1]
                folder = line[0]
                logging.info('Moving ' + file +
                             " back to it's orignial location")
                shutil.move(file, directory + '/' +
                            folder)
            elif 'mp4' in line[1]:
                old, ext = line[1].split('.')
                file = line[1]
                folder = line[0]
                logging.info(f"Moving {file} back to it's orignial location")
                shutil.move(old + ".mkv", directory + '/' +
                            folder)
            elif 'avi' in line[1]:
                old, ext = line[1].split('.')
                file = line[1]
                folder = line[0]
                logging.info(f"Moving {file} back to it's orignial location")
                shutil.move(old + ".mkv", directory + '/' +
                            folder)


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
