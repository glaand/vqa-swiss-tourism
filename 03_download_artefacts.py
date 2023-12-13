from slugify import slugify
import json
import urllib.request
import os
from time import sleep
import base64

# Load the responses.json file
with open('responses.json') as json_file:
    responses = json.load(json_file)

entries = []

# loop through the responses
for response in responses:
    try:
        slug = slugify(response['data']['name'])
        name = response['data']['name']
        description = response['data']['description']
        # base64 encode the description
        description = base64.b64encode(description.encode('utf-8')).decode('utf-8')
        latitude = 0
        longitude = 0
        category = ''
        if 'geo' in response['data']:
            if 'latitude' in response['data']['geo']:
                latitude = response['data']['geo']['latitude']
            if 'longitude' in response['data']['geo']:
                longitude = response['data']['geo']['longitude']
        photo = response['data']['photo']
        if 'category' in response['data']:
            category = response['data']['category']
        entries.append((slug, name, photo, description, latitude, longitude, category))
    except:
        continue

headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}

n = 0
for entry in entries:
    # create folder for each entry under ./artefacts
    folder = './artefacts/photos/'

    downloaded = False

    # download photo only if it doesn't exist
    if not os.path.exists(folder + f"/{entry[0]}.jpg"):
        try:
            downloaded = True
            req = urllib.request.Request(entry[2], headers=headers)
            with urllib.request.urlopen(req) as response, open(folder + f"/{entry[0]}.jpg", 'wb') as out_file:
                data = response.read() # a `bytes` object
                out_file.write(data)
        except:
            print('Error downloading photo for ' + entry[2])
    else:
        print('Photo already exists for ' + entry[0])

    if downloaded:
        sleep(1)
    n += 1
    print('Downloaded ' + str(n) + ' of ' + str(len(entries)))

filtered_entries = []
for entry in entries:
    slug, name, photo, description, latitude, longitude, category = entry
    filtered_entries.append((slug, name, category, latitude, longitude, description))

# save the entries to a csv file
import csv
with open('artefacts/metadata.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['slug', 'name', 'category', 'latitude', 'longitude', 'description'])
    writer.writerows(filtered_entries)