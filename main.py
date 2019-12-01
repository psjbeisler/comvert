import os
import tempfile
import patoolib

## System Variables
blacklist = '/opt/comvert/blacklist.ini'
type_in = '.cbr'
type_out = '.cbz'
wd = os.getcwd()

## User Options
# User INPUT format
# User OUTPUT format

## Logging
# Output Variables
# Sanity checks
# Start Logging

def extract_by_type():
    for f in os.scandir(wd):
        if f.name.endswith(type_in):
            global td
            td = tempfile.TemporaryDirectory()
            global n, e
            n, e = os.path.splitext(f.name)
            currentfile = os.path.join(wd, f.name)
            patoolib.extract_archive(currentfile, outdir=td.name)
            remove_blacklisted()
            create_new_archive()

def extract_by_name():
    pass

def remove_blacklisted():
    print('Checking Blacklist...')
    with open(blacklist, 'r') as bl:
        for spam in bl.read().splitlines():
            for root, dirs, files in os.walk(td.name):
                for file in files:
                    if file == spam:
                        spamfile = os.path.join(td.name, spam)
                        print('Removing: ' + spam)
                        os.remove(spamfile)

def create_new_archive():
    newfile = os.path.join(wd, n + type_out)
    print('Creating: ' + newfile)
    os.chdir(td.name)
    patoolib.create_archive(newfile, ['.'])

extract_by_type()

## Scan for Suspicious files

## Dont delete the new file if it has the same name

## Stats
## Optionally Notify
