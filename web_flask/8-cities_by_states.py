#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import base_model
from models import storage

""" Import modules """

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    This function will be called after each request.
    It closes the SQLAlchemy session to clean up resources.
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def list_states():
    """ states page """
    all_states = storage.all(State)
    return render_template("7-states_list.html", all_states=all_states)


@app.route('/cities_by_states', strict_slashes=False)
def list_cities_by_states():
    """ cities by states page """
    all_states = storage.all(State).values()
    return render_template('8-cities_by_states.html', all_states=all_states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
