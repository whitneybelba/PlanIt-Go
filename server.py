from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from api_call import search_yelp


app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
# app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Show search homepage."""

    return render_template("index.html")


@app.route("/results", methods=["GET"])
def get_choices():
    """Get user's restaurant, bar and activity genre choices."""

    location = request.args.get("location") + request.args.get("state")
    radius = request.args.get("radius")
    restaurant_categories = request.args.getlist("restaurant")
    bar_categories = request.args.getlist("bar")
    activity_categories = request.args.getlist("activity")

                ############################################
                #        yelp query for restaurants        #
                ############################################
    # iterates over list of categories selected from checkboxes, calls
    # the search_yelp function for each category, and appends the returned
    # list of restaurants in a category to a list for all restaurants
    restaurant_list = []
    for category in restaurant_categories:
        rest_results = search_yelp(category, location, radius)
        for restaurant in rest_results:
            categories = []
            for category in restaurant['categories']:
                categories.append(category[0])
            restaurant['category'] = ", ".join(categories)

        restaurant_list.append(rest_results)

                ############################################
                #            yelp query for bars           #
                ############################################
    bar_list = []
    for bar in bar_categories:
        bar_results = search_yelp(bar, location, radius)
        for bar in bar_results:
            categories = []
            for category in bar['categories']:
                categories.append(category[0])
            bar['category'] = ", ".join(categories)

        bar_list.append(bar_results)

                ############################################
                #         yelp query for activities        #
                ############################################

    activity_list = []
    for activity in activity_categories:
        activity_results = search_yelp(activity, location, radius)
        for activity in activity_results:
            categories = []
            for category in activity['categories']:
                categories.append(category[0])
            activity['category'] = ", ".join(categories)

        activity_list.append(activity_results)

    return render_template("results.html",
                           restaurant_list=restaurant_list,
                           bar_list=bar_list,
                           activity_list=activity_list)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
