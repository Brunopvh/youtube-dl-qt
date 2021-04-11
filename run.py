#!/usr/bin/env python3

import os

file_run = os.path.realpath(__file__)
path_run = os.path.dirname(file_run)
os.chdir(path_run)
work_dir = os.getcwd()

print(path_run)

os.chdir(path_run)
from youtube_dl_qt.__main__ import main
os.chdir(work_dir)

if __name__ == '__main__':
	main()