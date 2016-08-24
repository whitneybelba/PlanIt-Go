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
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

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
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    length = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    rest_id = db.Column(db.Integer)
    bar_id = db.Column(db.Integer)
    act_id = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Trip trip_id=%s name=%s>" % (self.trip_id,
                                              self.name)

# class Restaurant(db.Model):
#     """Info on restaurant."""

#     __tablename__ = "restaurants"

#     rest_id = db.Column(db.Integer,
#                           autoincrement=True,
#                           primary_key=True)
#     rest_name = db.Column(db.Integer,
#                          db.ForeignKey('movies.movie_id'))
#     rest_lat = db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     score = db.Column(db.Integer)

#     # Define relationship to user
#     user = db.relationship("User",
#                            backref=db.backref("ratings",
#                                               order_by=rating_id))

#     # Define relationship to movie
#     movie = db.relationship("Movie",
#                             backref=db.backref("ratings",
#                                                order_by=rating_id))

    def __repr__(self):
        """Provide helpful representation when printed."""        

#####################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."        