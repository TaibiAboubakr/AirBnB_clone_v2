#!/usr/bin/python3
""" Script that starts a Flask web application """
from flask import Flask, render_template
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


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template_page(n):
    """ Number template page """
    return render_template("5-number.html", num=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even_page(n):
    """ odd or even number page """
    if n % 2 == 0:
        return render_template("6-number_odd_or_even.html", num=n, type="even")
    else:
        return render_template("6-number_odd_or_even.html", num=n, type="odd")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
