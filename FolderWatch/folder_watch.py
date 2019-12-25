
import os
import sys
import time
import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


source = r"C:\Users\dell\Downloads" # Folder to watch
misc = "Others"

# Alias `os.path.join` to prevent frequent typing
p_proxy = os.path.join

# Map folders to expected file extensions
# Keys are the names of folders in Downloads folder
folders = dict(Music=['.wav','.mp3', '.aac'],
               Documents=['.pdf','.doc','.docx','.xls','.xlsx','.ppt','.pptx','.csv','.txt', '.md'],
               Compressed=['.zip','.7z','.rar'],
               Programs=['.msi','.exe'],
               Images=['.jpeg','.jpg','.png','.tiff','.svg','.ico','.gif'],
               Video=['.mp4','.avi','.mkv','.wmv','.ogg','.mov'])


class MyFileHandler(FileSystemEventHandler):
    """Handle File Modification events"""

    def on_modified(self, event):
        while 1:
            try:
                # My Downloads folder contains only folders, so use of `os.listdir` 
                # shouldn't ever cause memory issues
                for fn in os.listdir(source):
                    # Ignore temporary files
                    if os.path.isfile(p_proxy(source, fn)) and not \
                    (p_proxy(source, fn).endswith('.tmp') or p_proxy(source, fn).endswith('.crdownload')):    
                        # Get the file extension [hopefully, the file is reasonably named]           
                        fn_ = fn[fn.index('.'):].lower()
                        # Select a destination folder based on the file extension
                        for k,v in folders.items():
                            if fn_ in v:
                                dest_folder = k
                                break
                        else:
                            # Unrecognized/Miscellaneous file extensions
                            dest_folder = misc
                        
                        # Move the file to its appropriate folder
                        os.rename(p_proxy(source, fn), p_proxy(source, dest_folder, fn))

            # Wait for the file to finish downloading/copying or ignore if the file name
            # already exists
            except (PermissionError, FileNotFoundError, FileExistsError):
                time.sleep(1.5)
                continue
            else:
                break


def watch_folder():
    """Main Script that automatically moves downloaded files
       to their respective folders in the Downloads folder.
       Effectively prevents clutter.
    """

    observer = Observer()
    observer.schedule(MyFileHandler(), source, recursive=False)
    observer.start()

    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


# Prevent running when importing
watch_folder() if __name__ == "__main__" else None