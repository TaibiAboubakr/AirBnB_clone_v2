#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask
""" Import modules """

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def Home():
    """ Home page """
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def Hbnb_page():
    """ Hbnb page """
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
