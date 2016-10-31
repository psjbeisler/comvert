comvert
=====
A quick bash script to batch convert digital Comic Books to differnt formats.

Requires:

7-Zip - http://www.7-zip.org/

If ran without options, will convert all .cbr files to .cbz in current directory.

Usage:

    -s [ source directory ]
  
    -i [ input file type {cbr,cbz,cbt,cb7} ]
  
    -o [ output file type {cbz,cbt,cb7} ]
  
        7-Zip doesn't support .rar ouput
        
    -f [ filename ]

- Removes Thumbs.db from archive, if found
- Removes .DS_Store from archive, if found
- Removes Scan credit pages, if found
- Logs suspicious files not in the blacklist
( Please submit  a pull request for any new additions )

<a href="https://i.imgur.com/m06Js32"><img src="https://i.imgur.com/m06Js32l.png" title="source: imgur.com" /></a>
