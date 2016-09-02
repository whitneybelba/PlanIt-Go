from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from api_call import search_yelp
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Restaurant, Bar, Activity, Trip
from model import RestTrip, ActTrip, BarTrip



app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/search')
def index():
    """Show search page."""
    return render_template("index.html")


@app.route("/results", methods=["GET"])
def get_choices():
    """Get user's restaurant, bar and activity genre choices."""

    location = request.args.get("location") + request.args.get("state")
    radius = request.args.get("radius")
    restaurant_categories = request.args.getlist("restaurant")
    bar_categories = request.args.getlist("bar")
    activity_categories = request.args.getlist("activity")
    trip_name = request.args.get("name")

    user_id = session["user_id"]

    trip = Trip(user_id=user_id, name=trip_name, city=location[0:-3].title())

    db.session.add(trip)
    db.session.commit()


                 ##  yelp query for restaurants ##

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



                     ##  yelp query for bars  ##


    bar_list = []
    for category in bar_categories:
        bar_results = search_yelp(category, location, radius)
        for bar in bar_results:
            categories = []
            for category in bar['categories']:
                categories.append(category[0])
            bar['category'] = ", ".join(categories)

        bar_list.append(bar_results)



                 ##  yelp query for activities ##


    activity_list = []
    for category in activity_categories:
        activity_results = search_yelp(category, location, radius)
        for activity in activity_results:
            categories = []
            for category in activity['categories']:
                categories.append(category[0])
            activity['category'] = ", ".join(categories)

        activity_list.append(activity_results)

    return render_template("results.html",
                           restaurant_list=restaurant_list,
                           bar_list=bar_list,
                           activity_list=activity_list,
                           trip_id=trip.trip_id)


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
        return redirect("/")

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

@app.route('/', methods=['GET'])
def login_form():
    """Show login form."""

    if session.get('user_id'):
        return redirect("/profile")

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
        return redirect("/")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/")

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

    if session.get('user_id'):
        user_id = session["user_id"]
        user = User.query.get(user_id)
        name = user.first_name
        trips = user.trips

        return render_template("user_profile.html", user=name, trips=trips)

    else:
        flash("Please log in to view profile")
        return redirect("/")


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

@app.route('/trip/<int:trip_id>', methods=['GET'])
def show_trip(trip_id):
    """Show selected trip for user."""

    # user_id = session["user_id"]
    # user = User.query.filter_by(user_id=user_id).first()
    # restaurants = Restaurant.query.filter_by(trip_id=trip_id).all()
    # session["user_id"] = user.user_id
    # trips = user.trips
    trip = Trip.query.get(trip_id)

    return render_template("trip.html",
                           trip=trip)


                ############################################
                ##         add restaurant to trip         ##
                ############################################

@app.route('/add-restaurant', methods=['POST'])
def add_restaurant():
    """Add a restaurant to trip/itinerary."""

    name = request.form.get("name")
    url = request.form.get("url")
    city = request.form.get("location")
    lat = request.form.get("lat")
    long = request.form.get("long")
    rest_id = request.form.get("id")
    trip_id = request.form.get("trip_id")

    rest_trip = RestTrip(rest_id=rest_id, trip_id=trip_id)

    rest_record = db.session.query(Restaurant.rest_id).filter_by(rest_id=rest_id).first()
    if rest_record:
        db.session.add(rest_trip)
        db.session.commit()
    else:
        restaurant = Restaurant(rest_url=url,
                                rest_name=name,
                                rest_lat=lat,
                                rest_long=long,
                                rest_city=city,
                                rest_id=rest_id)

        db.session.add(restaurant)
        db.session.commit()
        db.session.add(rest_trip)
        db.session.commit()

    return jsonify({"rest_id": rest_id})


                ############################################
                ##      delete restaurant from trip       ##
                ############################################

@app.route('/delete-restaurant', methods=['POST'])
def delete_restaurant():
    """Delete a restaurant from trip/itinerary."""

    rest_id = request.form.get("id")
    trip_id = request.form.get("trip_id")

    rest_trip = db.session.query(RestTrip).filter_by(rest_id=rest_id,
                                                     trip_id=trip_id).one()
    db.session.delete(rest_trip)
    db.session.commit()


    return jsonify({"rest_id": rest_id})


                ############################################
                ##            add bar to trip             ##
                ############################################


@app.route('/add-bar', methods=['POST'])
def add_bar():
    """Add a bar to trip/itinerary."""

    name = request.form.get("name")
    url = request.form.get("url")
    city = request.form.get("location")
    lat = request.form.get("lat")
    long = request.form.get("long")
    bar_id = request.form.get("id")
    trip_id = request.form.get("trip_id")

    bar_trip = BarTrip(bar_id=bar_id, trip_id=trip_id)

    bar_record = db.session.query(Bar.bar_id).filter_by(bar_id=bar_id).first()
    if bar_record:
        db.session.add(bar_trip)
        db.session.commit()
    else:
        bar = Bar(bar_url=url,
                  bar_name=name,
                  bar_lat=lat,
                  bar_long=long,
                  bar_city=city,
                  bar_id=bar_id)

        db.session.add(bar)
        db.session.commit()
        db.session.add(bar_trip)
        db.session.commit()

    return jsonify({"bar_id": bar_id})


                ############################################
                ##          delete bar from trip          ##
                ############################################

@app.route('/delete-bar', methods=['POST'])
def delete_bar():
    """Delete a bar from trip/itinerary."""

    bar_id = request.form.get("id")
    trip_id = request.form.get("trip_id")

    bar_trip = db.session.query(BarTrip).filter_by(bar_id=bar_id,
                                                   trip_id=trip_id).one()
    db.session.delete(bar_trip)
    db.session.commit()

    return jsonify({"bar_id": bar_id})


                ############################################
                ##          add activity to trip          ##
                ############################################

@app.route('/add-activity', methods=['POST'])
def add_activity():
    """Add an activity to trip/itinerary."""

    name = request.form.get("name")
    url = request.form.get("url")
    city = request.form.get("location")
    lat = request.form.get("lat")
    long = request.form.get("long")
    act_id = request.form.get("id")
    trip_id = request.form.get("trip_id")

    act_trip = ActTrip(act_id=act_id, trip_id=trip_id)
    act_record = db.session.query(Activity.act_id).filter_by(act_id=act_id).first()

    if act_record:
        db.session.add(act_trip)
        db.session.commit()
    else:
        activity = Activity(act_url=url,
                            act_name=name,
                            act_lat=lat,
                            act_long=long,
                            act_city=city,
                            act_id=act_id)

        db.session.add(activity)
        db.session.commit()
        db.session.add(act_trip)
        db.session.commit()

    return jsonify({"act_id": act_id})


                ############################################
                ##       delete activity from trip        ##
                ############################################

@app.route('/delete-activity', methods=['POST'])
def delete_activity():
    """Delete an activity from trip/itinerary."""

    act_id = request.form.get("id")
    trip_id = request.form.get("trip_id")

    act_trip = db.session.query(ActTrip).filter_by(act_id=act_id,
                                                   trip_id=trip_id).one()
    db.session.delete(act_trip)
    db.session.commit()

    return jsonify({"act_id": act_id})


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app)
    app.jinja_env.auto_reload = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
