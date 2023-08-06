```
INSTALLATION

    $ pip3 install pagpdf

HELP

    $ pagpdf -h

USAGE

    $ pagpdf [-h] [-V] [-c] [-n] [-r] [-t] [-T] [file [file ...]]


Print number of PAGes in PDF files.

This simple utility prints file counter, number of pages and filename
for each given pdf file. Fields are separated by a '\t' (horizontal tab)
character.

Non-pdf files are silently skipped.

Empty or erroneous pdf files are reported as containing zero pages.

Examples:

    $ pagpdf * # list number of pages of all pdf files in current path

    $ pagpdf * 2>/dev/null # leave out warnings from pdfrw.PdfReader

POSITIONAL ARGUMENTS

  file                 files to be listed (non-pdf files are silently skipped)

OPTIONAL ARGUMENTS

  -h, --help           show this help message and exit
  -V, --version        show program's version number and exit
  -c, --csv-header     print CSV header as first line (default: don't)
  -n, --sort-by-pages  sort files by number of pages (default: sort by
                       filename)
  -r, --reverse        sort files in descending order (default: sort in
                       ascending order)
  -t, --total-too      print file list and total line (default: print file
                       list)
  -T, --total-only     print total line only (default: print file list)
```
