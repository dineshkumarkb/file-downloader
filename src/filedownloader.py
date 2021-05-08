import os
import requests
import socket
import shutil
from concurrent.futures import ThreadPoolExecutor


class FileDownloader(object):

    downloaded_files = 0

    def __init__(self, file_path: str):

        self.no_of_files = 0
        self.file_name = None

        if os.path.isfile(file_path):
            self.file_path = file_path
        else:
            raise TypeError(f" Invalid path: '{file_path}'. Please enter a valid file path ")

        self.is_valid = self.validate_file()

        if self.is_valid:
            self.start_download()
        else:
            raise FileNotFoundError(f" File doesnt exist or not found ")

    def validate_file(self):

        if os.path.exists(self.file_path):
            return True
        return False

    def start_download(self):

        with open(self.file_path, "r+") as download_file:
            contents = download_file.read().splitlines()

        cleaned_files = [x for x in contents if x != '']

        self.no_of_files = len(cleaned_files)

        print(f" Found {self.no_of_files} files for download..")

        with ThreadPoolExecutor(max_workers=5) as executor:
            for file_no, link in enumerate(cleaned_files, start=1):
                executor.submit(self.download_file, file_no=file_no, link=link)

        print(f" Download complete: {FileDownloader.downloaded_files} files succeeded of {self.no_of_files}..")

    def download_file(self, file_no, link):

        try:
            self.file_name = link.split("/")[-1]

            print(f" Downloading {self.file_name}[{file_no}/{self.no_of_files}] files....")

            response = requests.get(url=link, stream=True)
            if response.status_code == 200:
                print(f" Download successful for: {self.file_name} ")
                FileDownloader.downloaded_files += 1
                with open(self.file_name, 'wb') as output_file:
                    shutil.copyfileobj(response.raw, output_file)
            else:
                print(f" Download failed for: {self.file_name}")

        except (ConnectionError, socket.error) as e:
            print(f" Download failed for {self.file_name} with error {e}")


if __name__ == "__main__":
    f = FileDownloader(" Please enter your file name here ")
