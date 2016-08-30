import rauth
import os


def search_yelp(categories, location, radius):
    """Queries Yelp API using restaurant_category, location and radius as
        parameters and returns a list of businesses in that location."""

    # defining the parameters dict to be used when searching the Yelp API
    params = {}
    params["category_filter"] = categories
    params["location"] = location
    params["radius_filter"] = radius
    params["limit"] = "10"
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

    # data.values() of the JSON object returns a list of dictionaries
    # I want the 2nd index of that list to get the business info
    data_list = data.values()[2]

    return data_list
