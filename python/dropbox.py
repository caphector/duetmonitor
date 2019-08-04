#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dropbox, sys, os

path = sys.argv[1]

# Get your app key and secret from the Dropbox developer website
access_token = 'jlkyemerxk8r9ai'

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)

def main():
    transferData = TransferData(access_token)

    file_from = path
    file_to = '/3D printing/timelapse/' + path  # The full path to upload the file to, including the file name

    # API v2
    transferData.upload_file(file_from, file_to)

if __name__ == '__main__':
    main()