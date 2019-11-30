import os
from datetime import datetime

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from argparse import ArgumentParser


EXT = '.pdf'
parser = ArgumentParser(description="Merge or Split PDF files")

parser.add_argument('mode', 
                    choices=['merge', 'split'], 
                    type=str, 
                    help="The mode with which to the script. \
                          Should be either 'merge' or 'split'")
parser.add_argument('-f', '--filename', 
                    nargs='+', 
                    required=True,
                    type=str,
                    help="The filename(s) to be split/merged.\
                          For split mode, only one file is required; \
                          for merge mode, multiple files are obviously needed.")
parser.add_argument('-p', '--page', 
                    type=int,
                    help="[Split mode only]: The page at which to split the file")

args = parser.parse_args()

run_mode = args.mode
page = args.page
files = args.filename

def validate_args():
    """Validates the arguments passed"""

    if run_mode == 'merge':
        assert len(files) > 1, "Merge mode requires at least two PDF files"
        if page is not None:
            raise ValueError("Merge mode does not require page argument")
    
    # Implicit split mode
    else: 
        assert len(files) == 1, "Split mode requires at most one filename argument"
        if page is None:
            raise AttributeError("Split mode requires a page argument")
    
    # File validity check
    for f in files:
        assert os.path.isfile(f), f"{f} is not a valid file name/path"

        ext_start = f.index('.')
        assert f[(ext_start + 1):].lower().endswith('pdf'), f"{f} is not a PDF file"

def main():
    """Main script"""

    # Get the current date and time to allow for file-conflict 
    # avoidance when saving the generated files
    now = datetime.now().strftime('%y%m%d_%f')

    if run_mode == 'merge':
        output_file = os.path.join(os.getcwd(), f"merged_file_{now}{EXT}")
        
        # PDF merger object            
        merger = PdfFileMerger()

        for f in files:
            with open(f, 'rb') as f_:
                read_pdf = PdfFileReader(f_)
                merger.append(read_pdf)
        
        merger.write(output_file)

        # Ensures implicit split mode
        return
    
    # Split mode
    file = files[0]
    writer = PdfFileWriter()
    output_file = os.path.join(os.getcwd(), f"split_file_{now}_")

    with open(file, 'rb') as f:
        read_pdf = PdfFileReader(f)

        start = 0
        end = page

        if page >= read_pdf.numPages:
            raise ValueError("page argument should be less than the number of pages in the PDF file")

        # Create files
        for i in range(2):
            if i == 1:
                start = page
                end = read_pdf.numPages
                writer = PdfFileWriter()
            for p in range(start, end):
                p_obj = read_pdf.getPage(p)
                writer.addPage(p_obj)
      
            # Save each split file
            with open(f"{output_file}{str(i+1)}{EXT}", 'wb') as o_f:
                writer.write(o_f)
    
    

if __name__ == "__main__":
    validate_args()
    main()


