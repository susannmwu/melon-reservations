"""Models for melon reservation app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)

    reservations = db.relationship(
        "Reservation", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id}>"


class Reservation(db.Model):
    """A tasting reservation"""
    __tablename__ = "reservations"

    id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    date = db.Column(db.String, nullable=False)
    time = db.Column(db.Time, nullable=False)
    is_not_available = db.Column(db.Boolean, default=True)

    user = db.relationship("User", back_populates="reservations")

    def __repr__(self):
        return f"<Reservation id={self.id}, user_id={self.user_id}, time={self.time}>"

################################################################################################################
# Helper functions


def connect_to_db(flask_app, db_uri="postgresql:///melons", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
