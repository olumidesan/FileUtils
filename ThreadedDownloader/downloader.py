
import os
import time
import click
import requests

import urllib.parse as Parser

from tqdm import tqdm
from pprint import pprint
from utils import has_internet
from threading import Thread
from requests.exceptions import SSLError


SAVE_DIR = 'downloaded'
FULL_SAVE_PATH = os.path.join(os.getcwd(), SAVE_DIR)


class Downloader:
    """
    Class for downloading files given their urls
    :param source -> tuple: A tuple containing the url of the files to be downloaded

    :return -> None

    ***Later update***
    To-do: :param num_of_threads -> int: Number of threads to download each file with
    """

    # class methods
    all_threads = []
    CHUNK_SIZE = 1024 # 1MB
    MB_FACTOR = float(1 << 20)
    DEFAULT_FILE_NAME = 'unnamed_file'
    DEFAULT_FILE_SIZE = CHUNK_SIZE * 1e6 # 1GB

    def __init__(self, source:tuple=None): # num_of_threads:int):
        # self.num_of_threads = num_of_threads
        self.source = source

        self._session = requests.Session()
        self._initialize()
    
    def _initialize(self):
        """Initializes the downloader, creating threads for each pending url"""

        for url in self.source:
            self._create_download_thread(url)

    def start(self):
        """Starts the downloader"""

        for t in self.all_threads:
            t.start()

        for t in self.all_threads:
            t.join()

    def _create_download_thread(self, url):
        """Creates a thread where each download runs"""

        download_thread = Thread(target=self.download_from_source, args=(url,))
        self.all_threads.append(download_thread)    
    
    def _create_file_props(self, url):
        """Creates the file name and size of the file to be downloaded"""

        with self._session as s:
            try:
                resp = s.head(url)
                f_size = float(resp.headers.get('content-length'))
            except TypeError:
                raise 
            except SSLError:
                raise 

        f_name = url.rsplit('/', 1)[-1] if url.find('/') else self.DEFAULT_FILE_NAME  
        f_size = (float(f_size) / self.MB_FACTOR) * self.CHUNK_SIZE if f_size else self.DEFAULT_FILE_SIZE
        
        return f_name, f_size

    def _save_to_filesystem(self, resp, file_name, file_size):
        """Saves the file to the filesystem"""

        desc = f"Downloading {file_name}:"

        with open(os.path.join(FULL_SAVE_PATH, file_name), 'wb+') as fs:
            for chunk in tqdm(resp.iter_content(self.CHUNK_SIZE), desc=desc, total=int(file_size)):
                fs.write(chunk)           

    def download_from_source(self, url):
        """Downloads the file from ```url```and saves it to the filesystem"""

        file_name, file_size = self._create_file_props(url)
        with self._session as s:
            resp = s.get(url, stream=True)
            resp.raise_for_status()

        self._save_to_filesystem(resp, file_name, file_size)

    def __repr__(self):
        return format(vars(self))


@click.command()
# @click.option('-t','--threads', type=click.INT,  default=1, help="Number of threads to spawn")
@click.argument('source', type=click.STRING, nargs=-1, required=True)
def main(source): #, threads):
    """ source: url(s) of file(s) to be downloaded """

    if has_internet():
        downloader = Downloader(source) #, threads)
        downloader.start()
    else:
        click.echo("It looks like you have no internet connection. :( Kindly connect to the internet and try again.\n")

main() if __name__ == "__main__" else None


