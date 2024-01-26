#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask
from markupsafe import escape
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


@app.route('/c/<text>', strict_slashes=False)
def c_page(text):
    """ C page """
    return f"C {text}".replace("_", " ")


@app.route('/python/(<text>)', strict_slashes=False)
@app.route('/python', strict_slashes=False)
def python_page(text="is_cool"):
    """ Pyhton page """
    return f"Pyhton {text}".replace("_", " ")


@app.route('/number/<int:n>', strict_slashes=False)
def number_page(n):
    """ Number page """
    return f"{n} is a number"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
