import time
import rauth
import os


def search_yelp(categories, location):
    """Queries Yelp API using restaurant_category and location as parameters
        and returns a list of restaurants in that location."""

    # defining the parameters dict to be used when searching the Yelp API
    params = {}
    params["category_filter"] = categories
    params["location"] = "{}".format(location)
    params["radius_filter"] = "40000"
    params["limit"] = "12"
    params["sort"] = "2"

    ###########################################################################
    # setting up personal Yelp api keys and getting response object
    consumer_key = os.environ["YELP_CONSUMER_KEY"]
    consumer_secret = os.environ["YELP_CONSUMER_SECRET"]
    token = os.environ["YELP_ACCESS_TOKEN_KEY"]
    token_secret = os.environ["YELP_ACCESS_TOKEN_SECRET"]

    session = rauth.OAuth1Session(consumer_key=consumer_key,
                                  consumer_secret=consumer_secret,
                                  access_token=token,
                                  access_token_secret=token_secret)

    response = session.get("http://api.yelp.com/v2/search", params=params)
    session.close()

    ###########################################################################
    # transforming the data into JSON format and binding to 'data' variable
    data = response.json()

    time.sleep(1.0)

    # data.values() of the JSON object returns a list of dictionaries
    # I want the 2nd index of that list to get the business info
    data_list = data.values()[2]

    return data_list
