"""Utility file to seed trips database from seed_data/"""

from sqlalchemy import func

from model import User, Trip, Restaurant, Bar, Activity, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, first_name, last_name, email, password = row.split("|")

        user = User(user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_trips():
    """Load trips from u.trip into database."""

    print "Trips"

    for row in open("seed_data/u.trip"):
        row = row.rstrip()
        trip_id, name, city, length, user_id = row.split("|")

        trip = Trip(name=name,
                    city=city,
                    length=length,
                    user_id=user_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(trip)

    # Once we're done, we should commit our work
    db.session.commit()


def load_restaurants():
    """Load restaurants from u.restaurant into database."""

    print "Restaurants"

    for row in open("seed_data/u.restaurant"):
        row = row.rstrip()
        rest_id, rest_url, rest_name, rest_lat, rest_long, rest_city, trip_id = row.split("|")

        restaurant = Restaurant(rest_id=rest_id,
                                rest_url=rest_url,
                                rest_name=rest_name,
                                rest_lat=rest_lat,
                                rest_long=rest_long,
                                rest_city=rest_city,
                                trip_id=trip_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(restaurant)

    # Once we're done, we should commit our work
    db.session.commit()


def load_bars():
    """Load bars from u.bar into database."""

    print "Bars"

    for row in open("seed_data/u.bar"):
        row = row.rstrip()
        bar_id, bar_url, bar_name, bar_lat, bar_long, bar_city, trip_id = row.split("|")

        bar = Bar(bar_id=bar_id,
                  bar_url=bar_url,
                  bar_name=bar_name,
                  bar_lat=bar_lat,
                  bar_long=bar_long,
                  bar_city=bar_city,
                  trip_id=trip_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(bar)

    # Once we're done, we should commit our work
    db.session.commit()


def load_activities():
    """Load activities from u.activity into database."""

    print "Activities"

    for row in open("seed_data/u.activity"):
        row = row.rstrip()
        act_id, act_url, act_name, act_lat, act_long, act_city, trip_id = row.split("|")

        activity = Activity(act_id=act_id,
                            act_url=act_url,
                            act_name=act_name,
                            act_lat=act_lat,
                            act_long=act_long,
                            act_city=act_city,
                            trip_id=trip_id)

        # We need to add to the session or it won't ever be stored
        db.session.add(activity)

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_trips()
    load_restaurants()
    load_bars()
    load_activities()
    set_val_user_id()
