# comvert

A simple tool to batch convert digital Comic Books into different formats

```
usage: comvert.py [-h] [-i INPUT] [-o OUTPUT] [-s SOURCE]

Convert digital comic books

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input by file type
  -o OUTPUT, --output OUTPUT
                        output file type
  -s SOURCE, --source SOURCE
                        source directory
```
- Removes Thumbs.db from archive, if found
- Removes .DS_Store from archive, if found
- Removes ComicInfo.xml from archive, if found
- Removes scan credit pages, if found
