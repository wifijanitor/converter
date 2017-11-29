#!/usr/bin/env python3

import os, sys, errno
from sys import argv

'''
Script to use ffmpeg to transcode files to a smaller size
Files will be moved to "org" and then converted to mp4, with X.265 and aac encoding
and then stored in "conv"

Once this process has completed, the script will attempt to move the file from "conv"
back to the original location, and then delete the file in "org".

'''
# define where we want the files moved , so we can transcode locally

base=argv
org=os.path.expanduser('~/Movies/original/')
conv=os.path.expanduser('~/Movies/converted/')

#check that the directories exist, and if not create them

def path_exists():
	print("Checking if " + org + " and " + conv + " exist")
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

def main():
	print("exit")

if __name__ == '__main__':
	path_exists()
	main()