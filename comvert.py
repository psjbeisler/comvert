## Version 2 for cross-platform compatability

import os
import tempfile
import patoolib

## System Variables
blacklist = os.path.join(os.path.dirname(__file__), 'blacklist.ini')
type_in = '.cbr'
type_out = '.cbz'
cwd = os.getcwd()

## User Options
# User INPUT format
# User OUTPUT format

## Logging
# Output Variables
# Sanity checks
# Start Logging

def file_by_type():
    global f, td, comic, type
    for f in os.scandir(cwd):
        if f.name.endswith(type_in):
            td = tempfile.TemporaryDirectory()
            comic, type = os.path.splitext(f.name)
            extract_archive()

def file_by_name():
    pass

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
                        spamfile = os.path.join(td.name, spam)
                        print('found: ' + spam + ' in ' + comic)
                        os.remove(spamfile)

def create_archive():
    global newfile
    newfile = os.path.join(cwd, comic + type_out)
    os.chdir(td.name)
    patoolib.create_archive(newfile, ['.'])
    if newfile != currentfile:
        os.remove(currentfile)

file_by_type()
remove_blacklisted()
create_archive()

## Scan for Suspicious files

## Stats
## Optionally Notify
