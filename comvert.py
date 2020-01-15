#!/usr/bin/env python
"""Version 2 for cross-platform compatability"""

import os
import tempfile
import patoolib
import argparse

## System Variables
blacklist = os.path.join(os.path.dirname(__file__), 'blacklist.ini')
cwd = os.getcwd()

## User Options
parser = argparse.ArgumentParser(description='Convert some comic books.')
parser.add_argument('-i', '--input', action='store', default='.cbr',
                    help='select input by file type')
parser.add_argument('-o', '--output', action='store', default='.cbz',
                    help='select output file type')
args = parser.parse_args()

def file_by_name():
    pass

def file_by_type():
    global f, td, comic, type
    for f in os.scandir(cwd):
        if f.name.endswith(args.input):
            td = tempfile.TemporaryDirectory()
            comic, type = os.path.splitext(f.name)
            extract_archive()
            remove_blacklisted()
            create_archive()
            cleanup()

def extract_archive():
    global currentfile
    currentfile = os.path.join(cwd, f.name)
    patoolib.extract_archive(currentfile, outdir=td.name)

def remove_blacklisted():
    print('checking: ' + blacklist)
    with open(blacklist, 'r') as bl:
        for spam in bl.read().splitlines():
            for root, dirs, files in os.walk(td.name):
                for file in files:
                    if file == spam:
                        spamfile = os.path.join(root, file)
                        print('found: ' + spam + ' in ' + comic)
                        os.remove(spamfile)

def create_archive():
    global newfile, savfile
    newfile = os.path.join(cwd, comic + args.output)
    savfile = os.path.join(cwd, comic + '.sav')
    if os.path.exists(newfile):
        if os.path.exists(savfile):
            os.remove(savfile)
        os.rename(newfile, savfile)
    os.chdir(td.name)
    patoolib.create_archive(newfile, ['.'])

def cleanup():
    if newfile != currentfile:
        os.remove(currentfile)
    if os.path.exists(savfile):
        os.remove(savfile)

file_by_type()

## Scan for Suspicious files

## Stats
## Optionally Notify
