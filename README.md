comvert
=====
A quick bash script to batch convert digital Comic Books to differnt formats.

Requires:

7-Zip - http://www.7-zip.org/

If ran without options, will convert all .cbr files to .cbz in current directory

Usage:
  -s [ source directory ]
  -i [ input file type {cbr,cbz,cbt} ]
  -o [ output file type {cbz, cbt} ]

- Removes Thumbs.db from archive, if found
- Removes .DS_Store from archive, if found
- Removes Scan credit pages, if found and possible

<a href="http://imgur.com/XfMLch4"><img src="http://i.imgur.com/XfMLch4l.png" title="Hosted by imgur.com"/></a>
