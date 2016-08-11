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
def get_restaurant_choices():
    """Get user's restaurant genre choices."""

    restaurant_categories = request.args.getlist("restaurant")

    restaurant_list = []
    for restaurant in restaurant_categories:
        results = search_yelp(restaurant, "boulder")
        restaurant_list.append(results)

    return render_template("results.html",
                           restaurants=restaurant_list)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
