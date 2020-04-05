#!/usr/bin/env python
"""Version 2 for cross-platform compatability"""

import os
import tempfile
import argparse
import patoolib

def extract_archive():
    patoolib.extract_archive(currentfile, outdir=td.name)

def remove_blacklisted():
    print('comvert: Scanning ' + blacklist)
    with open(blacklist, 'r') as bl:
        for spam in bl.read().splitlines():
            for root, _, files in os.walk(td.name):
                for file in files:
                    if file == spam:
                        spamfile = os.path.join(root, file)
                        print('comvert: Removing' + spamfile)
                        os.remove(spamfile)

def create_archive():
    newfile = os.path.join(wd, comic + "." + args.output)
    bakfile = os.path.join(wd, comic + '.bak')
    if os.path.exists(newfile):
        if os.path.exists(bakfile):
            os.remove(bakfile)
        os.rename(newfile, bakfile)
    os.chdir(td.name)
    patoolib.create_archive(newfile, ['.'])
    os.chdir(wd)
    if newfile != currentfile:
        os.remove(currentfile)
    if os.path.exists(bakfile):
        os.remove(bakfile)

blacklist = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'blacklist.ini')
parser = argparse.ArgumentParser(description='Convert digital comic books')
parser.add_argument('-i', '--input', action='store', default='cbr', help='input by file type')
parser.add_argument('-o', '--output', action='store', default='cbz', help='output file type')
parser.add_argument('-s', '--source', action='store', default='.', help='source directory')
args = parser.parse_args()
wd = os.path.abspath(args.source)

for f in os.scandir(wd):
    if f.name.endswith(args.input):
        td = tempfile.TemporaryDirectory()
        comic, _ = os.path.splitext(f.name)
        currentfile = os.path.join(wd, f.name)
        extract_archive()
        remove_blacklisted()
        create_archive()
