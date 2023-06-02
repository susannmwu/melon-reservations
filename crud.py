"""CRUD operations"""


from model import db, User, Reservation, connect_to_db

if __name__ == '__main__':
    from server import app
    connect_to_db(app)


def create_user(username):
    """Create and return a new user."""

    user = User(username=username)

    return user


def get_user_by_username(username):
    """Return a user by username."""

    return User.query.filter(User.username == username).first()


def get_user_by_id(user_id):
    """Returns a user by user_id"""

    return User.query.get(user_id)


def create_reservation(user, date, time):
    """Create and return a reservation"""

    reservation = Reservation(user_id=user.user_id, date=date, time=time)
    db.session.add(reservation)
    db.session.commit()
    return reservation


def get_user_reservations(user_id):
    """Returns a list of user's reservations"""

    user_reservations = Reservation.query.filter(
        User.user_id == user_id).all()

    reservations_list = []

    for res in user_reservations:
        reservations_list.append(res)
    return reservations_list
