import json
from datetime import datetime
import os
from uuid import uuid4

arr = json.load(open('dataset/dataset.json'))

for film in arr['films']:
    new_name = uuid4().hex
    os.rename(film["video"], f'dataset/videos/{new_name}.mp4')
    os.rename(film["image"], f'dataset/images/{new_name}.webp')
    film['video'] = f'dataset/videos/{new_name}.mp4'
    film['image'] = f'dataset/images/{new_name}.webp'


json.dump(arr, open('dataset.json', 'w'))
