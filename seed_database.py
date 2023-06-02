"""Script to seed database."""

from flask import Flask

import os
import crud
import model
import server

app = Flask(__name__)

os.system("dropdb melons")
os.system("createdb melons")
model.connect_to_db(server.app)
model.db.create_all()


# create a new user

susan = crud.create_user("sus")
model.db.session.add(susan)
model.db.session.commit()
