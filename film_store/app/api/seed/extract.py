import json
import os
import sys
from datetime import datetime


def extract(data):
    res = {}
    try:
        res['name'] = data['name']
        res['description'] = data['description']
        # res['director'] = data['director']
        director = data['director']
        if type(director) == list:
            res['director'] = director[0]['name']
        else:
            res['director'] = director['name']

        res['datePublished'] = data['datePublished']
        res['genre'] = data['genre']
        res['price'] = 0
        res['duration'] = 0
        res['video'] = 0
        res['image'] = data['image']
    except Exception as e:
        return None
    return res


# dataset/*/*/*.json


total = 0
for root, dirs, files in os.walk("dataset"):
    for file in files:
        if file.endswith(".json"):
            total += 1

arr = []
progress = 0
for root, dirs, files in os.walk("dataset"):
    for file in files:
        if file.endswith(".json"):
            with open(os.path.join(root, file)) as json_file:
                data = json.load(json_file)
                res = extract(data)
                if res: arr.append(res)
                progress += 1

    if progress % 50 == 0:
        sys.stdout.write('\r')
        sys.stdout.write(f'Progress: {progress}/{total}')
        sys.stdout.flush()



# write to output.json
with open('output.json', 'w') as outfile:
    json.dump(arr, outfile)