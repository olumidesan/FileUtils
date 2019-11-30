## PDF Merge or Split
Merge or split PDF files

### Requirements
1. Python 3.5+
2. PyPDF2

### Usage
The script works directly from the command line, and in either of two modes: `merge` or `split`. 
That is, `ms.py [-h] -f FILENAME [FILENAME ...] [-p PAGE] {merge,split}`

To merge files, simply run `python3 ms.py merge --filename myfile.pdf yourfile.pdf herfile.pdf`
To split a PDF file, simply run `python3 ms.py split --filename myfile.pdf --page 5`

For more detailed help, type `python3 ms.py --help`
