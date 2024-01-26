"""
Created Date: 2024-01-Fr
Author: Lucas Barrez
-----
Last Modified: Friday, 26th January 2024 10:34:49 am
Modified By: Lucas Barrez
-----
HISTORY:
"""
from ftplib import FTP
import os
from io import BytesIO


class FTPservice:
    def __init__(self, hostname: str, username: str, pwd: str) -> None:
        self.hostname = hostname
        self.username = username
        self.pwd = pwd
        self.ftp = None

    def connect(self):
        try:
            self.ftp = FTP(self.hostname)
            self.ftp.login(user=self.username, passwd=self.pwd)
            self.ftp.set_pasv(True)
        except Exception as e:
            new_message = (
                "An error occurred while connecting to the server"
                f" ... {e}."
            )
            raise type(e)(new_message).with_traceback(e.__traceback__)


    def disconnect(self):
        if self.ftp:
            self.ftp.quit()
            print("disconnected")
    
    def set_binary_mode(self):
        self.ftp.voidcmd('TYPE I')

    def listing_files(self, path: str):
        listing = self.ftp.nlst(path)
        return listing
    
    def listing_details(self, path: str):
        self.set_binary_mode()
        details = []
        try:
            self.ftp.retrlines(f"MLSD {path}", details.append)
            return details
        except Exception as e:
            new_message = (
                "An error occured while getting directory details:"
                f" ... {e}."
            )
            raise type(e)(new_message).with_traceback(e.__traceback__)

    def download_file_content(self, remote_path: str, dest_path: str) -> bytes:
        content = b""
        try :
            with BytesIO() as buffer:
                self.ftp.retrbinary(f'RETR {remote_path}', buffer.write)
                content = buffer.getvalue()
            with open(dest_path, 'wb') as dest:
                dest.write(content)
            return content
        except Exception as e:
            new_message = (
                "An error occured while downloading file content"
                f" ... {e}."
            )
            raise type(e)(new_message).with_traceback(e.__traceback__)

    def download_all_files_recursive(self, remote_path: str, local_path: str):
        remote_details = self.listing_details(remote_path)
        try:
            os.makedirs(local_path, exist_ok=True)

            for detail in remote_details:
                detail_list = detail.split(";")
                type_char = ""
                name = "/"
                if len(detail_list) == 10 :
                    type_char = "dir"
                    name += str(detail_list[-1]).strip()

                if len(detail_list) == 11 :
                    type_char = "file"
                    name += str(detail_list[-1]).strip()

                remote_item_path = remote_path + name
                print(remote_item_path)
                local_item_path = (local_path + name).replace('/', "\\")

                if type_char == "file":
                    self.download_file_content(remote_item_path, local_item_path)
                    print(f'Downloaded: {remote_item_path}')

                elif type_char == "dir":
                    self.download_all_files_recursive(remote_item_path, local_item_path)
        except Exception as e:
            new_message = (
                "An error occured while downloading all files"
                f" ... {e}."
            )
            raise type(e)(new_message).with_traceback(e.__traceback__)