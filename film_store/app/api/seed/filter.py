import json
from datetime import datetime

data = json.load(open('output.json'))

# count of all genres
# {'Documentary': 3844, 'Short': 1422, 'Comedy': 15401, 'Sport': 1089, 'Music': 1710, 'Action': 6805, 'History': 2009, 'Horror': 5227, 'Romance': 8881, 'Fantasy': 3567, 'Sci-Fi': 3600, 'Drama': 24078, 'Family': 3553, 'Adventure': 4786, 'Crime': 6542, 'Western': 1149, 'Animation': 2129, 'Biography': 2368, 'Thriller': 9232, 'War': 2061, 'Mystery': 3730, 'Film-Noir': 494, 'Musical': 1382, 'News': 136, 'Talk-Show': 2, 'Adult': 14, 'Reality-TV': 9}

arr = []
max_each_year = 5
years = {}
min_year = 2011
max_genre_amount = 5

# filter corrupted images and vulgar words
filter_words = ['king', 'prey', 'black', 'thou', 'charles', 'air', 'zombie', 'nude', 'seyyit', 'camp', 'avatar', 'collided', 'blood', 'dune', 'eating', 'kurtaran', 'aus', 'dyke', 'cock', 'halbe', 'hell', 'earth', 'night', 'motel', 'road', 'people', 'baby', 'rental', 'genesis', 'dni', 'alan']

for film in data:
    if any([word in film['name'].lower() for word in filter_words]): continue

    if type(film['genre']) == str: # clean up single genre
        film['genre'] = [film['genre']]
    if len(film['genre']) > max_genre_amount: continue
    
    date = datetime.strptime(film['datePublished'], '%Y-%m-%d')
    year = date.year
    if year < min_year: continue

    if year not in years: years[year] = 0
    
    years[year] += 1
    if years[year] > max_each_year: continue

    arr.append(film)


genres = {}
for film in arr:
    for genre in film['genre']:
        if genre not in genres:
            genres[genre] = 0
        genres[genre] += 1

# min_each_genre = 3
# filter movies with genres that have less than min_each_genre movies
# for film in arr:
#     if any([genres[genre] < min_each_genre for genre in film['genre']]):
#         arr.remove(film)
print(len(arr))
print(genres)

json.dump(arr, open('output-filtered-genre.json', 'w'))



