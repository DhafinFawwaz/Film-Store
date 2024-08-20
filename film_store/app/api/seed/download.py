import os
import requests
import json
from datetime import datetime
import random
import faker

arr = json.load(open('output-filtered-genre.json'))

if not os.path.exists('images'):
    os.mkdir('images')
if not os.path.exists('videos'):
    os.mkdir('videos')

progress = 0

video_names = []
for (dirpath, dirnames, filenames) in os.walk("dataset/videos/"):
    video_names.extend(filenames)

for film in arr:
    try:
        # r = requests.get(film['image'])
        # with open(f'images/{film["name"]}.jpg', 'wb') as f:
        #     f.write(r.content)
        film['image'] = f'dataset/images/{film["name"]}.webp'
        film['video'] = f'dataset/videos/{video_names[progress]}'
        film['price'] = random.choice(range(300, 5001, 100))
        film['duration'] = random.choice(range(10, 7201, 1))
        
        progress += 1
    except Exception as e:
        print(f'Error: {e}')
    print(f'{progress}/{len(arr)}', end='\r')

dataset = {}
dataset["films"] = arr

all_genre = set()
for film in dataset["films"]:
    all_genre.update(film["genre"])
all_genre = list(all_genre)
dataset["genre"] = all_genre


def get_random_film_titles():
    min_film = 0
    max_film = 10
    if random.random() < 0.3:
        max_film = 0

    unique_idx = random.sample(range(0, len(arr)-1), random.randint(min_film, max_film))
    return [arr[i]["name"] for i in unique_idx]

f = faker.Faker()
user_amount = 30

def generate_user():
    fn = f.first_name()
    ln = f.last_name()
    return {
        "username": (fn+ln).lower(),
        "first_name": fn,
        "last_name": ln,
        "email": f.email(),
        "balance": random.choice(range(1000, 30001, 100)),
        "bought": get_random_film_titles(),
        "wishlist": get_random_film_titles()
    }
dataset["user"] = [
    generate_user()
    for i in range(user_amount)
]

def get_random_review():
    if random.random() < 0.3:
        return None
    return f.text()

def get_random_rating():
    if random.random() < 0.3:
        return None
    return random.choice(range(1, 11))

def get_random_review():
    return {
        "username": "",
        "film": "",
        "rating": "",
        "review": get_random_review(),
        "created_at": "",
    }

def get_random_date(year_start, year_end):
    year = random.randint(year_start, year_end)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{year}-{month}-{day} {hour}:{minute}:{second}"

max_review_per_film = user_amount
dataset["review"] = []
review_count = {}
for film in dataset["films"]:
    if random.random() < 0.2: continue # try to make atleast 20% of film has no review

    username_list = []
    username_list = random.sample([user["username"] for user in dataset["user"]], max_review_per_film)
    
    count = 0
    for username in username_list:
        r = random.random()
        if r < 0.25: # no review
            continue
        elif r < 0.5:
            # only rating
            count += 1
            review = {
                "username": username,
                "film": film["name"],
                "rating": random.randint(1, 5),
                "review": None,
                "created_at": get_random_date(2022, 2024),
            }
            dataset["review"].append(review)
        elif r < 0.75:
            # only review
            count += 1
            review = {
                "username": username,
                "film": film["name"],
                "rating": None,
                "review": f.text(),
                "created_at": get_random_date(2022, 2024),
            }
            dataset["review"].append(review)
        else:
            # rating and review
            count += 1
            review = {
                "username": username,
                "film": film["name"],
                "rating": random.randint(1, 5),
                "review": f.text(),
                "created_at": get_random_date(2022, 2024),
            }
            dataset["review"].append(review)


json.dump(dataset, open('dataset.json', 'w'))