import time
import rauth

import json
import os
import requests


def defineParams(location):
    params = {}
    params["term"] = "restaurants"
    params["category_filter"] = "french"
    params["location"] = "{}".format(location)
    params["radius_filter"] = "2000"
    params["limit"] = "20"
    params["sort"] = "2"

    return params

def getData(params):

    # setting up personal Yelp api keys
    consumer_key = os.environ["YELP_CONSUMER_KEY"]
    consumer_secret = os.environ["YELP_CONSUMER_SECRET"]
    token = os.environ["YELP_ACCESS_TOKEN_KEY"]
    token_secret = os.environ["YELP_ACCESS_TOKEN_SECRET"]

    session = rauth.OAuth1Session(consumer_key=consumer_key,
                                  consumer_secret=consumer_secret,
                                  access_token=token,
                                  access_token_secret=token_secret)

    response = session.get("http://api.yelp.com/v2/search", params=params)

    # transforming the data in JSON format
    data = response.json()
    session.close()

    return data

def main():

    locations = ["oakland"] #SF

    apiData = []
    for location in locations:
        params = defineParams(location)
        apiData.append(getData(params))
        time.sleep(1.0)

    #print len(apiData)

    for key in apiData[0].keys():
        print key

    for record in apiData:
        # print record["businesses"]
        print record["total"]
        # print record["region"]
    # print(json.dumps(apiData, sort_keys=True))
    return apiData[0]

# def get_restaurant_names():


#     data = main()
#     rest_name = data.values()[2][0]['name']

#     print rest_name
#     return rest_name



if __name__ == '__main__':
    main()