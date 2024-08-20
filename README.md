<h1 align="center" style="font-size: 2.5rem; font-weight: 700"><br>
  Seleksi Laboratorium Pemrograman<br>
  [Monolith Website]<br>
</h1>

# 👯 Author
|          Nama             |      NIM      |
| ------------------------- | ------------- |
| Dhafin Fawwaz Ikramullah  |    13522084   |

# 🌐 Deploy URL
Website URL: [https://filmstore-gokbzfw6.b4a.run](https://filmstore-gokbzfw6.b4a.run)

Please note that the website will sleep if there is no activity for 30 minutes. So if accessed while the website is sleeping, it will wake up first and can take around 20 - 60 seconds. Please wait.
If using chrome mobile, please update the chrome version to the newest version. It uses the new css unit called `dvh`. If not, it's still safe, it will fallback to vh unit.

# 🏃🏻‍♂️ How to Run
## Quick Start
Rename `.env.example` to `.env` and fill the environment variables as needed. It should already work with the default values, but you can change them if you want to.
Make sure you have docker and docker-compose installed on your machine.
Launch docker, then run the following command:
```
docker-compose up
```
This will take a while. It will build the images which are the database, redis, and the monolith website, run the containers, build tailwind files, collect static files, create admin account into the database, download the datasets, seeds the database, and finally start the website.
Once it says something like `Listening at: http://0.0.0.0:8001`, you can access the website on [http://127.0.0.1:8000/](http://127.0.0.1:8000/). 

## Quick Alternative
If you're on windows, you can also just double click the `run.bat`. It will rename the `.env.example` to `.env`, launch docker (then you need to click yes to enable administrator privilege), then run the `docker-compose up` command automatically. It depends if your docker is installed in `C:\Program Files\Docker\Docker\Docker Desktop.exe` though. If not, the `run.bat` file may not work.

## Troubleshoot
It's possible that you may see this error.
```
time="2024-08-20T11:33:05+07:00" level=warning msg="The \"POSTGRES_USER\" variable is not set. Defaulting to a blank string."
time="2024-08-20T11:33:05+07:00" level=warning msg="The \"POSTGRES_DB\" variable is not set. Defaulting to a blank string."
time="2024-08-20T11:33:05+07:00" level=warning msg="The \"SECRET_KEY\" variable is not set. Defaulting to a blank string."
time="2024-08-20T11:33:05+07:00" level=warning msg="The \"DB_HOST\" variable is not set. Defaulting to a blank string."
time="2024-08-20T11:33:05+07:00" level=warning msg="The \"DB_NAME\" variable is not set. Defaulting to a blank string."
time="2024-08-20T11:33:05+07:00" level=warning msg="The \"DB_USER\" variable is not set. Defaulting to a blank string."
time="2024-08-20T11:33:05+07:00" level=warning msg="The \"DB_PORT\" variable is not set. Defaulting to a blank string."
time="2024-08-20T11:33:05+07:00" level=warning msg="The \"DB_PASS\" variable is not set. Defaulting to a blank string."
env file <PATH TO PROJECT>\.env not found: CreateFile <PATH TO PROJECT>\.env: The system cannot find the file specified.
```
If this happens, it means you haven't renamed the `.env.example` to `.env`. Please rename it to `.env` and fill the environment variables as needed. It should already work with the default values, but you can change them if you want to.



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


# 🎥 Dataset

Dataset taken from

Images: [https://www.kaggle.com/datasets/rezaunderfit/48k-imdb-movies-data](https://www.kaggle.com/datasets/rezaunderfit/48k-imdb-movies-data)

Videos: [https://www.freepik.com/](https://www.freepik.com/)

Seeding the database took so much time and effort. The movies and images needs to be cleaned because of many inconsistency. The Videos needs to be hand picked for short videos because we're using free hosting here. Please appreciate it 😅

# 📍 Used Design Patterns

## Builder Pattern
According to [Refactoring Guru](https://refactoring.guru/design-patterns/builder) Builder Pattern is a creational design pattern that lets you construct complex objects step by step. The pattern allows you to produce different types and representations of an object using the same construction code.

Builder pattern is used in the APIResponse class. The APIResponse class is used to create a response object that will be returned by the API. This makes it really easy and clean to create a response object. We can chain multiple methods to either set the data, set the status code, set as error, error message, etc. Here is some section of the code that uses the builder pattern:

<div>
  <img src="./images/pattern/builder_pattern_1.png" width=49%>
  <img src="./images/pattern/builder_pattern_2.png" width=44%>
</div>

It can be used to easily create a response object. In the image, we chain it into setting cookies when user logged in. We chain it with error message and status code when there is an error. If we're not using the builder pattern, passing everything in the constructor and nulling the unused fields can be really messy and hard to read.


## Decorator Pattern
According to [Refactoring Guru](https://refactoring.guru/design-patterns/decorator) Decorator Pattern is a structural design pattern that lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors.

In python there's a built in way to implement this almost magically. We can use the `@` symbol to decorate a function. This is used in the APIView class. The APIView class is a class that is used to create an API endpoint. We can decorate it with `@protected`, `@public`, `@admin_only` to determine who can access the rest API. We can also decorate the class with the `@swagger` decorator to add the swagger documentation to the endpoint. As for frontend, there's also `@unauthorized` which can be used to redirect user to the home page if they are already logged in. Here is some section of the code that uses the decorator pattern:

<div>
  <img src="./images/pattern/decorator_pattern_1.png" width=48%>
  <img src="./images/pattern/decorator_pattern_2.png" width=49%>
</div>

As we can see, we're adding the `@swagger` decorator to the method to add the swagger documentation to the endpoint. We're also adding the `@admin_only` decorator to the method to make sure only admin can access the endpoint. This makes it really easy to add new behavior to the method without changing the method itself. Please note that this implementation of decorator pattern is specific to python. In other languages, we might need to create some wrapper interface to add new behavior to the object.



## Observer Pattern
According to [Refactoring Guru](https://refactoring.guru/design-patterns/observer) Observer Pattern is a behavioral design pattern that lets you define a subscription mechanism to notify multiple objects about any events that happen to the object they’re observing.

Observer pattern is used in some places in the project. One of them are for the database signals when some data is changed to invalidate cache and also in the client side javascript to add a behavior when user clicks a certain button. In django, we can use the `@receiver` decorator to add a function that will be called when a signal is sent. In javascript, we can use the `addEventListener` method to add a function that will be called when an event is triggered. These things are already built in to the framework/language. So we don't have to setup the observer pattern ourselves.

Here is some section of the code that uses the observer pattern:
<div>
  <img src="./images/pattern/observer_pattern_2.png" width=48%>
  <img src="./images/pattern/observer_pattern_1.png" width=42%>
</div>

As we can see, the models (database in general) don't need to know how to implement the cache invalidation. It just needs to send a signal to whatever is listening to it. In this case, the cache invalidation function is listening to the signal and will be called when the signal is sent. If in the future we want to do a certain behaviour when the data in database is changed, we just need to listen to the event through the `@receiver` decorator. This makes the code really clean and easy to read. The same goes for the client side javascript. The button doesn't need to know what to do when it's clicked. It just needs to send an event when it's clicked. The function that is listening to the event will be called when the event is triggered. This makes the code really clean and easy to read.


## Command Pattern
According to [Refactoring Guru](https://refactoring.guru/design-patterns/command) command pattern is a behavioral design pattern that turns a request into a stand-alone object that contains all information about the request. This transformation lets you pass requests as a method arguments, delay or queue a request’s execution, and support undoable operations.

Here is some section of the code that uses the command pattern:
<div>
  <img src="./images/pattern/command_pattern_1.png" width=48%>
  <img src="./images/pattern/command_pattern_2.png" width=40%>
</div>

As we can see in the image above, we can easily create a command by just inheriting the django built in base command class. Then we can easily call the command by running `python manage.py <COMMAND NAME>` like how we usually do it natively with django. This makes it really easy to create a command and run it.


# 💻 Technology Stack

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


# ✨ Bonus
| Nomor |          Bonus            | Dikerjakan |
| ----- | ------------------------- | ---------- |
| B01   | OWASP                     |            |
| B02   | Deployment                |     ✅     |
| B03   | Polling                   |     ✅     |
| B04   | Caching                   |     ✅     |
| B05   | Lighthouse                |            |
| B06   | Responsive Layout         |     ✅     |
| B07   | Dokumentasi API           |     ✅     |
| B08   | SOLID                     |     ✅     |
| B09   | Automated Testing         |            |
| B10   | Fitur Tambahan            |     ✅     |
| B11   | Ember                     |     ✅     |

## B01 OWASP
TBD


## B02 Deployment
Everything is deployed with a free service. Here are the services used:
- Database: PostgreSQL 14
- Caching: Redis 7.4.0
- REST API: Django Rest Framework 3.15.2

Website URL: [https://filmstore-gokbzfw6.b4a.run](https://filmstore-gokbzfw6.b4a.run)
Please note that the website will sleep if there is no activity for 30 minutes. So if accessed while the website is sleeping, it will wake up first and can take around 20 - 40 seconds. Please wait.
If using chrome mobile, please update the chrome version to the newest version. It uses the new css unit called `dvh`. If not, it's still safe, it will fallback to vh unit.

## B03 Polling
It's done by making the client do a request. Then the Backend Server will wait until there is new data available. If there is, it will return the data. If until around 30 seconds there is no new data, it will return an empty data and with 204 status code. The client will then wait for a few seconds and do the request again. Please note that only logged in user can do polling to reduce request.
Pages that use polling:
- / (Excluding the recommendation)
- /explore (including its search and paginated pages)
- /details/{id} (excluding the interactive star rating button)
- /details/{id}/review (including its paginated pages)
- /wishlist (including its search and paginated pages)
- /bought (including its search and paginated pages)

## B04 Caching
This is done with Redis. Result of some database queries that is frequently called will be cached. When the data is updated, the cache will be invalidated.
The caching is done for the following pages:
- / (Excluding the recommendation)
- /explore (including its search and paginated pages)
- /details/{id} (excluding the interactive star rating button)
- /details/{id}/review (including its paginated pages)
- /wishlist (including its search and paginated pages)
- /bought (including its search and paginated pages)

You can test this by looking at the print in the terminal. It will print `CACHE HIT` if the data is fetched from the cache, and `CACHE MISS` if the data is fetched from the database. There is also a print of the cache key that is used and the execution time.
Here is an example of the print:

<img src="./images/cache/cache_hit.png" alt="Cache Hit">
<img src="./images/cache/cache_miss.png" alt="Cache Miss">

## B05 Lighthouse
[Lighthouse](https://developer.chrome.com/docs/lighthouse/overview) is an open-source, automated tool for improving the quality of web pages. You can run it against any web page, public or requiring authentication. It has audits for performance, accessibility, progressive web apps, SEO, and more.
#### Login
<div>
  <img src="./images/lighthouse/login_m.png" width=49%>
  <img src="./images/lighthouse/login_d.png" width=49%>
</div>

#### Register
<div>
  <img src="./images/lighthouse/register_d.png" width=49%>
  <img src="./images/lighthouse/register_m.png" width=49%>
</div>

#### Home
<div>
  <img src="./images/lighthouse/home_d.png" width=49%>
  <img src="./images/lighthouse/home_m.png" width=49%>
</div>

#### Explore
<div>
  <img src="./images/lighthouse/explore_d.png" width=49%>
  <img src="./images/lighthouse/explore_m.png" width=49%>
</div>

#### Details
<div>
  <img src="./images/lighthouse/details_d.png" width=49%>
  <img src="./images/lighthouse/details_m.png" width=49%>
</div>

#### Review
<div>
  <img src="./images/lighthouse/review_d.png" width=49%>
  <img src="./images/lighthouse/review_m.png" width=49%>
</div>

#### Wishlist
<div>
  <img src="./images/lighthouse/wishlist_d.png" width=49%>
  <img src="./images/lighthouse/wishlist_m.png" width=49%>
</div>

#### Bought
<div>
  <img src="./images/lighthouse/bought_d.png" width=49%>
  <img src="./images/lighthouse/bought_m.png" width=49%>
</div>

#### Profile
<div>
  <img src="./images/lighthouse/profile_d.png" width=49%>
  <img src="./images/lighthouse/profile_m.png" width=49%>
</div>

#### Watch
<div>
  <img src="./images/lighthouse/watch_d.png" width=49%>
  <img src="./images/lighthouse/watch_m.png" width=49%>
</div>


## B06 Responsive Layout
Website styling is created with Tailwind CSS. It is responsive and can be viewed on any device. Here are some screenshots of the website on different devices:
#### Login
<div>
  <img src="./images/responsive/login_sm.png" width=12.5%>
  <img src="./images/responsive/login_md.png" width=26%>
  <img src="./images/responsive/login_lg.png" width=57%>
</div>

#### Register
<div>
  <img src="./images/responsive/register_sm.png" width=12.5%>
  <img src="./images/responsive/register_md.png" width=26%>
  <img src="./images/responsive/register_lg.png" width=57%>
</div>

#### Home
<div>
  <img src="./images/responsive/home_sm.png" width=12.5%>
  <img src="./images/responsive/home_md.png" width=26%>
  <img src="./images/responsive/home_lg.png" width=57%>
</div>

#### Explore
<div>
  <img src="./images/responsive/explore_sm.png" width=12.5%>
  <img src="./images/responsive/explore_md.png" width=26%>
  <img src="./images/responsive/explore_lg.png" width=57%>
</div>

#### Details
<div>
  <img src="./images/responsive/details_sm.png" width=12.5%>
  <img src="./images/responsive/details_md.png" width=26%>
  <img src="./images/responsive/details_lg.png" width=57%>
</div>

#### Details 2
<div>
  <img src="./images/responsive/details2_sm.png" width=12.5%>
  <img src="./images/responsive/details2_md.png" width=26%>
  <img src="./images/responsive/details2_lg.png" width=57%>
</div>

#### Review
<div>
  <img src="./images/responsive/review_sm.png" width=12.5%>
  <img src="./images/responsive/review_md.png" width=26%>
  <img src="./images/responsive/review_lg.png" width=57%>
</div>

#### Wishlist
<div>
  <img src="./images/responsive/wishlist_sm.png" width=12.5%>
  <img src="./images/responsive/wishlist_md.png" width=26%>
  <img src="./images/responsive/wishlist_lg.png" width=57%>
</div>

#### Bought
<div>
  <img src="./images/responsive/bought_sm.png" width=12.5%>
  <img src="./images/responsive/bought_md.png" width=26%>
  <img src="./images/responsive/bought_lg.png" width=57%>
</div>

#### Profile
<div>
  <img src="./images/responsive/profile_sm.png" width=12.5%>
  <img src="./images/responsive/profile_md.png" width=26%>
  <img src="./images/responsive/profile_lg.png" width=57%>
</div>

#### Watch
<div>
  <img src="./images/responsive/watch_sm.png" width=12.5%>
  <img src="./images/responsive/watch_md.png" width=26%>
  <img src="./images/responsive/watch_lg.png" width=57%>
</div>

## B07 Dokumentasi API
API Documentation is created with Swagger. You can access the documentation on either

Swagger: [https://filmstore-gokbzfw6.b4a.run/swagger](https://filmstore-gokbzfw6.b4a.run/swagger)

Redoc: [https://filmstore-gokbzfw6.b4a.run/redoc](https://filmstore-gokbzfw6.b4a.run/redoc)

Note that in some cases, the documentation might take a long time to respond.


## B08 SOLID
### Single Responsibility Principle
According to [Samuel Oloruntoba and Anish Singh Walia](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design) Single-responsibility Principle (SRP) states a class should have one and only one reason to change, meaning that a class should have only one job.

Example of the implementation is for the models. It can be seen in the image below.

<div>
  <img src="./images/solid/single_responsibility_2.png" width=100%>
  <img src="./images/solid/single_responsibility_1.png" width=45%>
  <img src="./images/solid/single_responsibility_3.png" width=40%>
</div>

As we can see, the Film model is only responsible for the film data. If we want to serialize the film object to a python dict which is serializable to json, we create a new class called FilmRequestSerializer. We're not adding a new function inside the Film model class. If we want to do a cache invalidation when saving, we're not overriding the save method in the Film model class. We're using signals and make a function listen to it. This way, the Film model class follows the Single Responsibility Principle.


### Open/Closed Principle
According to [Samuel Oloruntoba and Anish Singh Walia](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design) Open-closed Principle (OCP) states objects or entities should be open for extension but closed for modification.

Example of the implementation is for the model serializer. It can be seen in the image below.

<div>
  <img src="./images/solid/openclosed_1.png" width=100%>
</div>

As we can se in the image, we previously already have a FilmResponseSerializer. Then we want to create a new formated version for it that is used to render the html using template engine. One way to do it is by modifying the FilmResponseSerializer and create an if else check inside it. But that will violate the Open/Closed Principle. Instead, we create a new class called FilmViewContextSerializer which inherits from the FilmResponseSerializer. Then it will format the duration to format `hh:mm:ss` and limits the genre array visually. This way, we're extending the FilmResponseSerializer class without modifying it. Therefore, the FilmResponseSerializer class follows the Open/Closed Principle.


### Liskov Substitution Principle
According to [Samuel Oloruntoba and Anish Singh Walia](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design) Liskov Substitution Principle states let q(x) be a property provable about objects of x of type T. Then q(y) should be provable for objects y of type S where S is a subtype of T.

Example of the implementation is for the overrided user model. It can be seen in the image below.

<div>
  <img src="./images/solid/liskov_substitution_1.png" width=100%>
  <img src="./images/solid/liskov_substitution_2.png" width=100%>
</div>

As we can see in the image above, the GeneralUser class inherits the AbstractUser class which is a built-in class in Django. The GeneralUser class is used to override the AbstractUser class to add a new field called balance. For example, the method that populates user from API Request is used everywhere inside some decorators. Because it follows the Liskov Substitution Principle, we don't need to modify that method and everything will just work as initially.


### Interface Segregation Principle
According to [Samuel Oloruntoba and Anish Singh Walia](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design) The interface segregation principle states a client should never be forced to implement an interface that it doesn’t use, or clients shouldn’t be forced to depend on methods they do not use.

Example of the implementation is for the model serializer. It can be seen in the image below.

<div>
  <img src="./images/solid/interface_segregation_1.png" width=100%>
</div>

As we can see in the image, the APIFilmDetail class implements the http methods for GET, PUT, and DELETE. It's not forced to implement other methods like POST or PATCH. This way, the APIFilmDetail class follows the Interface Segregation Principle.


### Dependency Inversion Principle
According to [Samuel Oloruntoba and Anish Singh Walia](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design) Dependency inversion principle states entities must depend on abstractions, not on concretions. It states that the high-level module must not depend on the low-level module, but they should depend on abstractions.

<div>
  <img src="./images/solid/dependency_inversion_2.png" width=100%>
  <img src="./images/solid/dependency_inversion_1.png" width=45%>
  <img src="./images/solid/liskov_substitution_2.png" width=45%>
</div>

As we can see in the image above, we're not directly touching the JWT class when populating the user in the request object. We're using the Token class which is an abstraction for the JWT class which is the lower level module. This way, if we want to change the type of token, we can just create another class that inherits from the Token class and implement the methods. Then simply swap the JWT to that class when creating the Auth object. This way, the Token class follows the Dependency Inversion Principle.



## B09 Automated Testing
Automated Unit Test is done with Django's built-in testing framework. The tests are located in the `tests.py` file in each app. The tests are run with the following command:
```
docker-compose run web python manage.py test
```
TBD (screenshots)

## B10 Fitur Tambahan
The additional features done are:
#### 1. Film Recommendation
<div>
  <img src="./images/responsive/home_sm.png" width=12.5%>
  <img src="./images/responsive/home_md.png" width=26%>
  <img src="./images/responsive/home_lg.png" width=57%>
</div>

#### 2. Rating & Review
<div>
  <img src="./images/responsive/details_sm.png" width=12.5%>
  <img src="./images/responsive/details_md.png" width=26%>
  <img src="./images/responsive/details_lg.png" width=57%>
</div>
<div>
  <img src="./images/responsive/review_sm.png" width=12.5%>
  <img src="./images/responsive/review_md.png" width=26%>
  <img src="./images/responsive/review_lg.png" width=57%>
</div>

#### 3. Wishlist
<div>
  <img src="./images/responsive/wishlist_sm.png" width=12.5%>
  <img src="./images/responsive/wishlist_md.png" width=26%>
  <img src="./images/responsive/wishlist_lg.png" width=57%>
</div>


## B11 Ember
Ember/Bucket is used for the deployment to store image and video files. The bucket used is supabase.



# 🌐 API Endpoints

Detailed API documentation can be accessed on either

Swagger: [https://filmstore-gokbzfw6.b4a.run/swagger](https://filmstore-gokbzfw6.b4a.run/swagger)

Redoc: [https://filmstore-gokbzfw6.b4a.run/redoc](https://filmstore-gokbzfw6.b4a.run/redoc)

## Version: v1

**Contact information:**  
dhafin.fawwaz@gmail.com  


## Endpoints
| Route | Method | Description |
| -------- | ----------- | ----------- |
| /films | GET | Get all films |
| /films | POST | Upload a new film |
| /films/{id} | GET | Get a film details by ID |
| /films/{id} | PUT | Update a film |
| /films/{id} | DELETE | Delete a film |
| /login | POST | Login a user |
| /polling/bought | GET | Polling search bought film |
| /polling/details/{id} | GET | Polling get film details |
| /polling/details/{id}/review | GET | Polling get film reviews |
| /polling/film | GET | Polling search film |
| /polling/wishlist | GET | Polling search wishlist film |
| /register | POST | Register a user |
| /self | GET | Get current user data |
| /users | GET | Get all users |
| /users/{id} | GET | Get user by ID |
| /users/{id} | DELETE | Delete user by ID |
| /users/{id}/balance | POST | Modify a user's balance |



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

