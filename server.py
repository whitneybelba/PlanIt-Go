from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from api_call import search_yelp
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Restaurant, Bar, Activity, Trip


app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


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
                ##       yelp query for restaurants       ##
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
                ##           yelp query for bars          ##
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
                ##        yelp query for activities       ##
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


                ############################################
                ##           show register form           ##
                ############################################

@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register.html")


                ############################################
                ##         process register form          ##
                ############################################

@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    first_name = request.form["fname"]
    last_name = request.form["lname"]

    check = User.query.filter_by(email=email).first()
    if check:
        flash("Already a user, please login")
        return redirect("/login")

    else:
        new_user = User(email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name)

        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(email=email).first()
        name = user.first_name
        trips = user.trips

        flash("User %s added." % email)
        return render_template("user_profile.html", user=name, trips=trips)


                ############################################
                ##             show login form            ##
                ############################################

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login.html")


                ############################################
                ##           process login form           ##
                ############################################

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id
    name = user.first_name
    trips = user.trips

    flash("Logged in")
    return render_template("user_profile.html", user=name, trips=trips)


                ############################################
                ##            show profile page           ##
                ############################################

@app.route('/profile', methods=['GET'])
def show_profile():
    """Show profile page."""

    user_id = session["user_id"]
    user = User.query.filter_by(user_id=user_id).first()
    name = user.first_name
    trips = user.trips

    return render_template("user_profile.html", user=name, trips=trips)


                ############################################
                ##                 logout                 ##
                ############################################

@app.route('/logout')
def logout():
    """Log out user from session"""

    del session["user_id"]
    flash("You are now logged out")
    return redirect("/")


                ############################################
                ##           show selected trip           ##
                ############################################

@app.route('/trip', methods=['GET'])
def show_trip():
    """Show selected trip for user."""

    user_id = session["user_id"]
    user = User.query.filter_by(user_id=user_id).first()
    restaurants = db.session.query(Restaurant).filter_by.all()
    session["user_id"] = user.user_id
    trips = user.trips

    return render_template("trip.html",
                           trips=trips,
                           restaurants=restaurants)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app)
    app.jinja_env.auto_reload = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
