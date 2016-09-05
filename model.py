"""Models and database functions for Trip Itinerary project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#####################################################################
# Model definitions


class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id,
                                               self.email)


class Trip(db.Model):
    """Trip that user can save."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(40), nullable=False)
    length = db.Column(db.String(40), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # Define relationship to restaurants, bars, activities and user
    restaurants = db.relationship("Restaurant",
                                  secondary="restaurants_trips",
                                  backref="trips")

    bars = db.relationship("Bar",
                           secondary="bars_trips",
                           backref="trips")

    activities = db.relationship("Activity",
                                 secondary="activities_trips",
                                 backref="trips")

    user = db.relationship("User", backref=db.backref("trips"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "%s" % self.name


class Restaurant(db.Model):
    """Info on restaurant."""

    __tablename__ = "restaurants"

    rest_id = db.Column(db.String(100), primary_key=True)
    rest_url = db.Column(db.String(300), nullable=False)
    rest_name = db.Column(db.String(40), nullable=False)
    rest_lat = db.Column(db.String(50), nullable=False)
    rest_long = db.Column(db.String(40), nullable=False)
    rest_city = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "%s, %s, %s" % (self.rest_name, self.rest_url, self.rest_city)


class RestTrip(db.Model):
    """Specific restaurant in a trip."""

    __tablename__ = "restaurants_trips"

    rest_trip_id = db.Column(db.Integer,
                             autoincrement=True,
                             primary_key=True)
    rest_id = db.Column(db.String(100),
                        db.ForeignKey('restaurants.rest_id'),
                        nullable=False)
    trip_id = db.Column(db.Integer,
                        db.ForeignKey('trips.trip_id'),
                        nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "%s" % (self.rest_id)


class Bar(db.Model):
    """Info on bar."""

    __tablename__ = "bars"

    bar_id = db.Column(db.String(100), primary_key=True)
    bar_url = db.Column(db.String(300), nullable=False)
    bar_name = db.Column(db.String(40), nullable=False)
    bar_lat = db.Column(db.String(40), nullable=False)
    bar_long = db.Column(db.String(40), nullable=False)
    bar_city = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "%s" % (self.bar_name)


class BarTrip(db.Model):
    """Specific bar in a trip."""

    __tablename__ = "bars_trips"

    bar_trip_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    bar_id = db.Column(db.String(100),
                       db.ForeignKey('bars.bar_id'),
                       nullable=False)
    trip_id = db.Column(db.Integer,
                        db.ForeignKey('trips.trip_id'),
                        nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "%s" % (self.bar_id)


class Activity(db.Model):
    """Info on bar."""

    __tablename__ = "activities"

    act_id = db.Column(db.String(100), primary_key=True)
    act_url = db.Column(db.String(300), nullable=False)
    act_name = db.Column(db.String(40), nullable=False)
    act_lat = db.Column(db.String(40), nullable=False)
    act_long = db.Column(db.String(40), nullable=False)
    act_city = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "%s" % (self.act_name)


class ActTrip(db.Model):
    """Specific activity in a trip."""

    __tablename__ = "activities_trips"

    act_trip_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    act_id = db.Column(db.String(100),
                       db.ForeignKey('activities.act_id'),
                       nullable=False)
    trip_id = db.Column(db.Integer,
                        db.ForeignKey('trips.trip_id'),
                        nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "%s" % (self.act_id)


                #################################
                ##       Helper functions      ##
                #################################


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database
    db.app = app
    db.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///trips'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.create_all()


if __name__ == "__main__":
    # As a convenience, if you run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
