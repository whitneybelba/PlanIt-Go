"""Models and database functions for Ratings project."""

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
    restaurants = db.relationship("Restaurant", backref=db.backref("trips"))
    bars = db.relationship("Bar", backref=db.backref("trips"))
    activities = db.relationship("Activity", backref=db.backref("trips"))
    user = db.relationship("User", backref=db.backref("trips"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Trip trip_id=%s name=%s>" % (self.trip_id,
                                              self.name)


class Restaurant(db.Model):
    """Info on restaurant."""

    __tablename__ = "restaurants"

    rest_id = db.Column(db.String(100), primary_key=True)
    rest_name = db.Column(db.String(40), nullable=False)
    rest_lat = db.Column(db.String(50), nullable=False)
    rest_long = db.Column(db.String(40), nullable=False)
    rest_city = db.Column(db.String(40), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Restaurant rest_id=%s name=%s>" % (self.rest_id,
                                                    self.rest_name)


class Bar(db.Model):
    """Info on bar."""

    __tablename__ = "bars"

    bar_id = db.Column(db.String(100), primary_key=True)
    bar_name = db.Column(db.String(40), nullable=False)
    bar_lat = db.Column(db.String(40), nullable=False)
    bar_long = db.Column(db.String(40), nullable=False)
    bar_city = db.Column(db.String(40), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Bar bar_id=%s name=%s>" % (self.bar_id,
                                            self.bar_name)


class Activity(db.Model):
    """Info on bar."""

    __tablename__ = "activities"

    act_id = db.Column(db.String(100), primary_key=True)
    act_name = db.Column(db.String(40), nullable=False)
    act_lat = db.Column(db.String(40), nullable=False)
    act_long = db.Column(db.String(40), nullable=False)
    act_city = db.Column(db.String(40), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Activity act_id=%s name=%s>" % (self.act_id,
                                                 self.act_name)

                #################################
                #        Helper functions       #
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
