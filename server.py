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

    location = request.args.get("location")
    radius = request.args.get("radius")

    restaurant_categories = request.args.getlist("restaurant")
    # iterates over list of categories selected from checkboxes, calls
    # the search_yelp function for each category, and appends the returned
    # list of restaurants in a category to a list for all restaurants
    restaurant_list = []
    for category in restaurant_categories:
        rest_results = search_yelp(category, location, radius)
        restaurant_list.append(rest_results)

    bar_categories = request.args.getlist("bar")
    bar_list = []
    for bar in bar_categories:
        bar_results = search_yelp(bar, location, radius)
        bar_list.append(bar_results)

    activity_categories = request.args.getlist("activity")
    activity_list = []
    for activity in activity_categories:
        activity_results = search_yelp(activity, location, radius)
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
