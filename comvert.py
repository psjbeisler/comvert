#!/usr/bin/env python
"""Version 2 for cross-platform compatability"""

import os
import tempfile
import argparse
import patoolib

def extract_archive(archive, temp):
    patoolib.extract_archive(archive, outdir=temp)

def remove_blacklisted(temp):
    print('comvert: Scanning ' + blacklist)
    with open(blacklist, 'r') as bl:
        for spam in bl.read().splitlines():
            for root, _, files in os.walk(temp):
                for file in files:
                    if file == spam:
                        spamfile = os.path.join(root, file)
                        print('comvert: Removing' + spamfile)
                        os.remove(spamfile)

def create_archive(source, title, type_in, type_out, temp):
    newfile = os.path.join(source, title + "." + type_out)
    curfile = os.path.join(source, title + "." + type_in)
    bakfile = os.path.join(source, title + '.bak')
    if os.path.exists(newfile):
        if os.path.exists(bakfile):
            os.remove(bakfile)
        os.rename(newfile, bakfile)
    os.chdir(temp)
    patoolib.create_archive(newfile, ['.'])
    os.chdir(source)
    if newfile != curfile:
        os.remove(curfile)
    if os.path.exists(bakfile):
        os.remove(bakfile)

def repack_archive(path):
    for f in os.scandir(path):
        if f.name.endswith(args.input):
            orig_name, _ = os.path.splitext(f.name)
            curfile = os.path.join(path, orig_name + "." + args.input)
            newfile = os.path.join(path, orig_name + "." + args.output)
            if newfile == curfile:
                print("Can't repack a file to the same format")
                return
            patoolib.repack_archive(curfile, newfile)
            os.remove(curfile)

def main(path):
    for f in os.scandir(path):
        if f.name.endswith(args.input):
            orig_temp = tempfile.TemporaryDirectory()
            orig_name, _ = os.path.splitext(f.name)
            orig_full = os.path.join(path, f.name)
            extract_archive(orig_full, orig_temp.name)
            remove_blacklisted(orig_temp.name)
            create_archive(path, orig_name, args.input, args.output, orig_temp.name)

blacklist = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'blacklist.ini')
parser = argparse.ArgumentParser(description='Convert digital comic books')
parser.add_argument('-i', '--input', action='store', default='cbr', help='input by file type')
parser.add_argument('-o', '--output', action='store', default='cbz', help='output file type')
parser.add_argument('-s', '--source', action='store', default='.', help='source directory')
parser.add_argument('-p', '--preserve', action='store_true', help='Preserve archive')
args = parser.parse_args()
here = os.path.abspath(args.source)
if args.preserve:
    repack_archive(here)
else:
    main(here)
