# comvert

A simple tool to batch convert digital Comic Books into different formats

```
usage: comvert.py [-h] [-i INPUT] [-o OUTPUT] [-s SOURCE] [-p]

Convert digital comic books

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file type
  -o OUTPUT, --output OUTPUT
                        output file type
  -s SOURCE, --source SOURCE
                        source directory
  -p, --preserve        Preserve archive

```
# blacklist
Enabled by default
- Removes Thumbs.db from archive, if found
- Removes .DS_Store from archive, if found
- Removes ComicInfo.xml from archive, if found
- Removes scan credit pages, if found
- `--preserve` disables this feature
