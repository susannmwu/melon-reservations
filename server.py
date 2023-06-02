"""Server for melon tasting reservation scheduler."""

from flask import Flask, render_template, redirect, request, flash, session
from model import connect_to_db, db
from datetime import date, timedelta

from jinja2 import StrictUndefined

import requests
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

TIMES = ["12:00 AM", "12:30 AM", "1:00 AM", "1:30 AM", "2:00 AM", "2:30 AM", "2:30 AM", "3:00 AM",
         "3:30 AM", "4:00 AM", "4:30 AM", "5:00 AM", "5:30 AM", "6:00 AM", "6:30 AM", "7:00 AM", "7:30 AM",
         "8:00 AM", "8:30 AM", "9:00 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM",
         "1:00 PM", "1:30 PM", "2:00 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM",
         "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM", "9:00 PM", "9:30 PM", "10:00 PM",
         "11:00 PM", "11:30 PM"]

start_date = date(2023, 5, 30)
end_date = date(2024, 5, 30)

delta = end_date - start_date

day_list = []

for item in range(delta.days + 1):
    day = start_date + timedelta(days=item)

    # day_list.append(day.strftime("%B %d, %Y"))

    day_list.append(day)


@app.route("/")
def homepage():
    """View homepage."""
    return render_template("homepage.html")


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    username = request.form.get("username")

    user = crud.get_user_by_username(username)

    if user:
        flash("Cannot create an account with that username. Please try again.")

    else:
        user = crud.create_user(username)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please login")
    return redirect("/")


@app.route("/user_profile")
def show_user_reservations():
    """View user reservations"""

    if "username" in session:
        logged_in_username = session["username"]
        user = crud.get_user_by_username(logged_in_username)
        user_id = user.user_id

        return redirect(f"/users/{user_id}")
    else:
        flash("Please log in to view your reservations")
        return ("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details of a user."""
    user = crud.get_user_by_id(user_id)

    return render_template("user-reservations.html", user=user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    username = request.form.get("username")
    user = crud.get_user_by_username(username)

    if not user:
        flash("The username is incorrect.")
    else:
        session["username"] = user.username
        flash(f"Welcome back, {user.username}!")
    return redirect("/")


@app.route("/reservations")
def search():
    """Search for a reservation"""

    return render_template("reservations.html", times=TIMES, day_list=day_list)


@app.route("/schedule-tasting", methods=["POST"])
def schedule_tasting():

    logged_in_username = session.get("username")
    user = crud.get_user_by_username(logged_in_username)

     
    time = request.form.get("time")
    day = request.form.get("day")

    reservation = crud.create_reservation(user, day, time)

    if logged_in_username is None:
        flash("You must log in to make a reservation")

    else:
        db.session.add(reservation)
        db.session.commit()

        flash(f"Sucess! You've made a reservation")

    return render_template("user-reservations.html", user=user)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
