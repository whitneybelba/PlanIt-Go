# PlanIt+Go
PlanIt+Go is an interactive travel activity organizer that utilizes the Yelp API and allows users to research and save a list of restaurants, bars and activities/sights that they would like to visit while on vacation. 

Learn more about the developer: www.linkedin.com/in/whitneybelba/


## Technology Stack

* Python
* Yelp API
* Flask
* Jinja2
* PostgresSQL
* SQLAlchemy
* Javascript/jQuery
* AJAX
* HTML
* CSS
* Bootstrap

##Get PlanIt+Go Running Locally

Clone or fork this repo: 

```
https://github.com/whitneybelba/PlanIt-Go

```

Create and activate a virtual environment inside your project directory: 

```

virtualenv env

source env/bin/activate

```

Install the requirements:

```
pip install -r requirements.txt

```

Get your own secret keys from Yelp (https://www.yelp.com/developers) and save them to a file <kbd>secrets.sh</kbd>. You should also set your own secret key for Flask. Your file should look something like this:

```
export CONSUMER_KEY='YOURCONSUMERKEYHERE'
export CONSUMER_SECRET='YOURCONSUMERSECRETKEYHERE'
export TOKEN='YOURTOKENHERE'
export TOKEN_SECRET='YOURTOKENSECRETHERE'

```
    
Source your secret keys:

```
source secrets.sh

```

Run the server:

```
python server.py

```
Navigate to `localhost:5000/home` to be able to create your own account and search

## Login and Search
After a user logs in, he or she is able to search a US city that they would like to travel to, and pick the types of restaurants, bars and activities/sites that they would like to visit on their trip. After the app queries the Yelp API, the user is supplied with a list of options that relates to their preferences.  From there they can research and compare the options and decide which ones they would like to add to a trip/itinerary. Once the user has added all desired options, they can view their saved itinerary. Users are able search as many categories as they would like, add as many options as they would like to a trip, and save as many trips as they would like to their profile. 

![alt text](/static/img/login_ss.png "Login Screen/Homepage")

![alt text](/static/img/profile.png "User Profile Page")

![alt text](/static/img/search.png "Search Page")

![alt text](/static/img/results.png "Results Page")

![alt text](/static/img/trip.png "Trip Details Page")

## Version 2.0
The next steps I am taking are to add maps to saved trips via the Google Maps API, to refactor Python code for faster API querying and to add OAuth/Google sign in for password handling.
