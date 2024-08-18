<h1 align="center" style="font-size: 2.5rem; font-weight: 700"><br>
  Seleksi Laboratorium Pemrograman<br>
  [Monolith Website]<br>
</h1>

# 👯 Author
|          Nama             |      NIM      |
| ------------------------- | ------------- |
| Dhafin Fawwaz Ikramullah  |    13522084   |

# Deploy URL
[https://filmstore-gokbzfw6.b4a.run](https://filmstore-gokbzfw6.b4a.run)

# 🏃🏻‍♂️ How to Run
## Quick Start
Rename `.env.example` to `.env` and fill the environment variables as needed. It should already work with the default values, but you can change them if you want to.
Make sure you have docker and docker-compose installed on your machine.
Launch docker, then run the following command:
```
docker-compose up
```
This will take a while. It will build the images which are the database, redis, and the monolith website, run the containers, build tailwind files, collect static files, insert admin to database, download the datasets, seeds the database, and finally start the website.
Once it says something like `Listening at: http://0.0.0.0:8001`, you can access the website on [http://127.0.0.1:8000/](http://127.0.0.1:8000/). 

## Run Database
If you just want to run the database, you can run the following command:
```
docker-compose up database
```

## Run Redis
If you just want to run the redis, you can run the following command:
```
docker-compose up redis
```

## Run Monolith Website
If you just want to run the backend, make sure both database and redis is running. Then run the following command:
```
docker-compose up web
```


# Used Design Patterns
<!-- Design pattern yang digunakan dan alasannya,  -->

APIResponse Builder Pattern
APIView, protected, swagger Decorator


# Technology Stack

## Development
- Monolith Website: Django 5.1
- Database: PostgreSQL 14
- Caching: Redis 7.4.0
- REST API: Django Rest Framework 3.15.2

## Deployment
- Monolith Website: Django 5.1
- Monolith Website Host: Back4App
- Database Host: Supabase (PostgreSQL)
- Caching Host: Redis Cloud (Redis)


# API Endpoints
API Documentation for Film Store

## Version: v1

**Contact information:**  
dhafin.fawwaz@gmail.com  

### Security
**Bearer**  

|apiKey|*API Key*|
|---|---|
|Name|Authorization|
|In|header|

### /films

#### GET
##### Summary:

Get all films

##### Description:

Query parameter 'q' can be used to search for films by title (case-insensitive)

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| q | query | Search for films by title and director | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | object |
| 400 |  | object |
| 401 |  | object |

#### POST
##### Summary:

Upload a new film

##### Description:

A new film will be uploaded to the database and the response will contain the films url instead of the binary file

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| title | formData | The title of the film | Yes | string |
| description | formData | A brief description of the film | Yes | string |
| director | formData | The director of the film | Yes | string |
| release_year | formData | The year the film was released | Yes | integer |
| genre | formData | A list of genres | Yes | [ string ] |
| price | formData | The price of the film | Yes | number |
| duration | formData | In seconds | Yes | integer |
| video | formData | The video file | Yes | file |
| cover_image | formData | The cover image of the film | No | file |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | object |
| 400 |  | object |
| 401 |  | object |

### /films/{id}

#### GET
##### Summary:

Get a film details by ID

##### Description:

the id in the url is the film's ID primary key

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | object |
| 400 |  | object |
| 401 |  | object |

#### PUT
##### Summary:

Update a film

##### Description:

The film data will be updated in the database and the response will contain the films url instead of the binary file

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |
| title | formData | The title of the film | Yes | string |
| description | formData | A brief description of the film | Yes | string |
| director | formData | The director of the film | Yes | string |
| release_year | formData | The year the film was released | Yes | integer |
| genre | formData | A list of genres | Yes | [ string ] |
| price | formData | The price of the film | Yes | number |
| duration | formData | In seconds | Yes | integer |
| video | formData | The video file. If not provided, the video will not be updated | No | file |
| cover_image | formData | The cover image of the film. If not provided, the cover image will not be updated | No | file |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | object |
| 400 |  | object |
| 401 |  | object |

#### DELETE
##### Summary:

Delete a film

##### Description:

A new film will be uploaded to the database and the response will contain the films url instead of the binary file

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |
| title | formData | The title of the film | Yes | string |
| description | formData | A brief description of the film | Yes | string |
| director | formData | The director of the film | Yes | string |
| release_year | formData | The year the film was released | Yes | integer |
| genre | formData | A list of genres | Yes | [ string ] |
| price | formData | The price of the film | Yes | number |
| duration | formData | In seconds | Yes | integer |
| video | formData | The video file. If not provided, the video will not be updated | No | file |
| cover_image | formData | The cover image of the film. If not provided, the cover image will not be updated | No | file |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | object |
| 400 |  | object |
| 401 |  | object |

### /login

#### POST
##### Summary:

Login a user

##### Description:

The user will be logged in and a token will be returned

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | object |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | object |
| 400 |  | object |

### /polling/bought

#### GET
##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /polling/details/{id}

#### GET
##### Summary:

Polling get film details

##### Description:

Will response when new data is available.

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | object |
| 204 |  | object |

### /polling/details/{id}/review

#### GET
##### Summary:

Polling get film reviews

##### Description:

Find film reviews by page. Will response when new data is available.

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /polling/film

#### GET
##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /polling/wishlist

#### GET
##### Description:



##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 |  |

### /register

#### POST
##### Summary:

Register a user

##### Description:

The user will be registered and a token will be returned

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| data | body |  | Yes | object |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 201 |  | object |
| 400 |  | object |

### /self

#### GET
##### Summary:

Get current user data

##### Description:

Get the current user data by the auth token

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | object |
| 400 |  | object |
| 401 |  | object |

### /users

#### GET
##### Summary:

Get all users

##### Description:

Get all users in the database

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| q | query | Search for a user by username | No | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | object |
| 400 |  | object |
| 401 |  | object |

### /users/{id}

#### GET
##### Summary:

Get user by ID

##### Description:

Get user by ID

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | object |
| 400 |  | object |
| 401 |  | object |

### /users/{id}/balance

#### POST
##### Summary:

Modify a user's balance

##### Description:

Change a user's balance by ID

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string |

##### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 |  | object |
| 400 |  | object |
| 401 |  | object |


# Bonus
| Nomor |          Bonus            | Dikerjakan |
| ----- | ------------------------- | ---------- |
| B01   | OWASP                     |     ✅     |
| B02   | Deployment                |     ✅     |
| B03   | Polling                   |     ✅     |
| B04   | Caching                   |     ✅     |
| B05   | Lighthouse                |     ✅     |
| B06   | Responsive Layout         |     ✅     |
| B07   | Dokumentasi API           |     ✅     |
| B08   | SOLID                     |     ✅     |
| B09   | Automated Testing         |     ✅     |
| B10   | Fitur Tambahan            |     ✅     |
| B11   | Ember                     |     ✅     |

## B01 OWASP
## B02 Deployment
Everything is deployed with a free service. Here are the services used:
- Database: PostgreSQL 14
- Caching: Redis 7.4.0
- REST API: Django Rest Framework 3.15.2

Website URL: [https://filmstore-gokbzfw6.b4a.run](https://filmstore-gokbzfw6.b4a.run)
Please note that the website will sleep if there is no activity for 30 minutes. So if accessed while the website is sleeping, it will wake up first and can take around 20 - 40 seconds. Please wait.
If using chrome mobile, please update the chrome version to the newest version. It uses the new css unit called `dvh`. If not, it's still safe, it will fallback to vh unit.

## B03 Polling
It's done by making the client do a request. Then the Backend Server will wait until there is new data available. If there is, it will return the data. If until around 30 seconds there is no new data, it will return an empty data and with 204 status code. The client will then wait for a few seconds and do the request again.
Pages that use polling:
- / (Excluding the recommendation)
- /explore (including its search and paginated pages)
- /details/{id}
- /details/{id}/review (including its paginated pages)
- /wishlist (including its search and paginated pages)
- /bought (including its search and paginated pages)

## B04 Caching
This is done with Redis. Result of some database queries that is frequently called will be cached. When the data is updated, the cache will be invalidated.
The caching is done for the following pages:
- / (Excluding the recommendation)
- /explore (including its search and paginated pages)
- /details/{id}
- /details/{id}/review (including its paginated pages)
- /wishlist (including its search and paginated pages)
- /bought (including its search and paginated pages)

You can test this by looking at the print in the terminal. It will print `CACHE HIT` if the data is fetched from the cache, and `CACHE MISS` if the data is fetched from the database. There is also a print of the cache key that is used and the execution time.
Here is an example of the print:

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
  <img src="./images/cache_hit.png" alt="Cache Hit">
  <img src="./images/cache_miss.png" alt="Cache Miss">
</div>

## B05 Lighthouse

## B06 Responsive Layout
Website styling is created with Tailwind CSS. It is responsive and can be viewed on any device. Here are some screenshots of the website on different devices:
#### Login
<div>
  <img src="./images/login_sm.png" width=12.5%>
  <img src="./images/login_md.png" width=26%>
  <img src="./images/login_lg.png" width=57%>
</div>

#### Register
<div>
  <img src="./images/register_sm.png" width=12.5%>
  <img src="./images/register_md.png" width=26%>
  <img src="./images/register_lg.png" width=57%>
</div>

#### Home
<div>
  <img src="./images/home_sm.png" width=12.5%>
  <img src="./images/home_md.png" width=26%>
  <img src="./images/home_lg.png" width=57%>
</div>

#### Explore
<div>
  <img src="./images/explore_sm.png" width=12.5%>
  <img src="./images/explore_md.png" width=26%>
  <img src="./images/explore_lg.png" width=57%>
</div>

#### Details
<div>
  <img src="./images/details_sm.png" width=12.5%>
  <img src="./images/details_md.png" width=26%>
  <img src="./images/details_lg.png" width=57%>
</div>

#### Details 2
<div>
  <img src="./images/details2_sm.png" width=12.5%>
  <img src="./images/details2_md.png" width=26%>
  <img src="./images/details2_lg.png" width=57%>
</div>

#### Review
<div>
  <img src="./images/review_sm.png" width=12.5%>
  <img src="./images/review_md.png" width=26%>
  <img src="./images/review_lg.png" width=57%>
</div>

#### Wishlist
<div>
  <img src="./images/wishlist_sm.png" width=12.5%>
  <img src="./images/wishlist_md.png" width=26%>
  <img src="./images/wishlist_lg.png" width=57%>
</div>

#### Bought
<div>
  <img src="./images/bought_sm.png" width=12.5%>
  <img src="./images/bought_md.png" width=26%>
  <img src="./images/bought_lg.png" width=57%>
</div>

#### Profile
<div>
  <img src="./images/profile_sm.png" width=12.5%>
  <img src="./images/profile_md.png" width=26%>
  <img src="./images/profile_lg.png" width=57%>
</div>



## B07 Dokumentasi API
## B08 SOLID
## B09 Automated Testing
## B10 Fitur Tambahan
## B11 Ember