#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask, render_template
from models.state import State
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


@app.route('/states', strict_slashes=False)
def list_states():
    """ states page """
    all_states = storage.all(State)
    return render_template("9-states.html", all_states=all_states)


@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    """ states by id page """
    all_states = storage.all(State).values()
    for state in all_states:
        if state.id == id:
            return render_template('9-states.html', state=state)
    return render_template('9-states.html')


if __name__ == "__main__":
    storage.reload()
    app.run(host='0.0.0.0', port=5000)
