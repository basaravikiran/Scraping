from bs4 import BeautifulSoup
from urlparse import urlparse
import re
import requests
import os

url1 = 'https://en.wikipedia.org/wiki/Transhumanism/'
url2 = 'http://pythonforengineers.com/pythonforengineersbook/'
url3 = 'http://www.eenadu.net'
url4 = 'https://offerilla.com/'

# Assign url to be tested
url = url3

# get contents from url
content = requests.get(url).content

# extract base url
parsed_uri = urlparse(url)
base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

# get soup
soup = BeautifulSoup(content, 'lxml')  # lxml parser

# find the tag
image_tags = soup.findAll('img')

# file to write image URLs #
fh1 = open('urllist.txt', 'w')
# fix image URLs
for image_tag in image_tags:
    image_url = image_tag.get("src")
    if not image_url.startswith('http'):
        if re.match(r'//[\w]', image_url):
            image_url = 'http:'+image_url
        elif re.match(r'/[\w]', image_url):
            image_url = base_url + image_url[1:]
        else:
            image_url = base_url + image_url
# Find Image File Name
    image_path = os.path.split(image_url)
    image_file_long = image_path[1]
    image_file_long_split = image_file_long.rsplit('.')
    image_file_no_ext = image_file_long_split[0]
    extension = image_file_long_split[-1][0:3]
    image_file = image_file_no_ext+'.'+extension
    extension = extension.lower()
    image = requests.get(image_url)
# Write data and urls to files
    if extension in ['png', 'jpg', 'svg', 'gif', 'ico']:
        with open(image_file, "wb") as fh2:
            fh2.write(image.content)
        fh2.close()
        fh1.writelines(image_url)
        fh1.writelines('\n')
fh1.close()
