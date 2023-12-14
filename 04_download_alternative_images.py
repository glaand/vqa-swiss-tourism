from slugify import slugify
import json
import urllib.request
import os
from time import sleep
import base64
import sys

# Load the responses.json file
with open('responses.json') as json_file:
    responses = json.load(json_file)

images_to_download = []

# loop through the responses
for response in responses:
    slug = slugify(response['data']['name'])
    if slug == sys.argv[1]:
        for image in response['data']['image']:
            images_to_download.append(image['url'])
        break

headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}

folder = f"./alternative-images/photos/{sys.argv[1]}"
if not os.path.exists(folder):
    os.makedirs(folder)

n = 0
for image in images_to_download:
    downloaded = False

    # download photo only if it doesn't exist
    if not os.path.exists(folder + f"/{n}.jpg"):
        try:
            downloaded = True
            req = urllib.request.Request(image, headers=headers)
            with urllib.request.urlopen(req) as response, open(folder + f"/{n}.jpg", 'wb') as out_file:
                data = response.read() # a `bytes` object
                out_file.write(data)
        except:
            print('Error downloading photo for ' + image)
    else:
        print('Photo already exists for ' + n)

    if downloaded:
        sleep(1)
    n += 1
    print('Downloaded ' + str(n) + ' of ' + str(len(images_to_download)))
