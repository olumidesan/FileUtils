
import os
import sys
import time
import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

folders = dict(Music=['.wav','.mp3', '.aac'],
               Documents=['.pdf','.doc','.docx','.xls','.xlsx','.ppt','.pptx','.csv','.txt', '.md'],
               Compressed=['.zip','.7z','.rar'],
               Programs=['.msi','.exe'],
               Images=['.jpeg','.jpg','.png','.tiff','.svg','.ico','.gif'],
               Video=['.mp4','.avi','.mkv','.wmv','.ogg','.mov', 'webm'])


source = r"C:\Users\dell\Downloads"
misc = "Others"

# Alias `os.path.join` to prevent frequent typing
p_proxy = os.path.join

class MyFileHandler(FileSystemEventHandler):
    """Handle File Modification events"""

    def on_modified(self, event):
        while 1:
            try:
                # My Downloads folder contains only folders, so this shouldn't 
                # ever cause memory issues
                for fn in os.listdir(source):
                    if os.path.isfile(p_proxy(source, fn)) and not \
                    (p_proxy(source, fn).endswith('.tmp') or p_proxy(source, fn).endswith('.crdownload')):               
                        fn_ = f".{fn.rsplit('.', 1)[-1].lower()}"
                        for k,v in folders.items():
                            if fn_ in v:
                                dest_folder = k
                                break
                        else:
                            dest_folder = misc
                        os.rename(p_proxy(source, fn), p_proxy(source, dest_folder, fn))
            except (PermissionError, FileNotFoundError, FileExistsError):
                # Wait for the file to finish downloading/copying
                time.sleep(1)
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
