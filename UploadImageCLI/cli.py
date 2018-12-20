"""
Main module for command line to upload images
"""
import os
import base64
import requests
from cmd import Cmd

version = "1.0"

usage = """
=================================
Contoso Library book image upload
=================================
Usage:

upload <full path to filename> <Function URL>
help
version
exit
======================
"""
class UploadImagePrompt(Cmd):
    """
    Implementation of the upload image prompt
    """
    @classmethod
    def do_exit(cls, args):
        """Exits the program."""
        print ("Exiting.")
        raise SystemExit

    @classmethod
    def do_upload(cls, args):
        """
        Triggers the image upload function to Azure blob store.
        """
        arguments = args.split()
        if len(arguments)!=2:
            print("Wrong syntax. Provide a filename and the HTTP trigger function URL")
        filename = arguments[0]
        http_url = arguments[1]
        upload_image(filename, http_url)

    @classmethod
    def do_usage(cls, args):
        """
        Displays the usage
        """
        print(usage)

    @classmethod
    def do_version(cls, args):
        """
        Displays the version
        """
        print(version)

def upload_image(filepath, http_url):
    """
    Construct HTTP POST request and issue to function URL
    """
    with open(filepath, "rb") as image_file:
        encoded_image_string = base64.b64encode(image_file.read())  

    # Extract filename and extension    
    filename_w_ext = os.path.basename(filepath)
    filename, fileext = os.path.splitext(filename_w_ext)
    imageext = fileext[1:]  #fileext returns .jpg so getting the ext only
    http_param = {'image_type':imageext}

    requests.post(http_url, params=http_param, data=encoded_image_string)


if __name__ == '__main__':
    print(usage)
    PROMPT = UploadImagePrompt()
    PROMPT.prompt = 'Contoso_Library_ImageScanner> '
    PROMPT.cmdloop('Waiting for files...')
