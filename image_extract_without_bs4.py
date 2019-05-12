"""
This script extracts images from a URL and saves them
in downloaded_images folder created in same folder the script copied to.
The URL to be extracted should be passed as command line argument
example: python image_extract.py  http://www.eenadu.net
"""

import sys
import os
import requests
from lxml import html
from urllib.parse import urljoin


class ImageScrape:
    """
    Methods to download images for a given web page and
    save them locally

    """
    def __init__(self):
        """
        Creating folder to download images
        """
        if not os.path.exists('downloaded_images'):
            try:
                os.mkdir('downloaded_images')
            except OSError:
                print("Creation of the directory failed\n")
            else:
                print("Successfully created the directory\n")

    def extract_images(self):
        """
        Downloads images from a given URL to downloaded_images folder
        """
        base_url = sys.argv[1]
        print('Extracting images from {} \n'.format(base_url))
        response = requests.get(base_url)
        tree = html.fromstring(response.content)
        image_urls = tree.xpath("//img/@src")
        if not image_urls:
            sys.exit("No Images were found in the given URL")
        absolute_image_urls = [urljoin(response.url, url) for url in image_urls]
        print(absolute_image_urls, '\n', len(image_urls))
        for url in absolute_image_urls:
            img_resp = requests.get(url)
            file_stream = open('downloaded_images/{}'.format(url.split('/')[-1]), 'wb')
            file_stream.write(img_resp.content)
            file_stream.close()

if __name__ == '__main__':
    testobj = ImageScrape()
    testobj.extract_images()
