from flask import Blueprint, render_template

# create main blueprint
main = Blueprint("main", __name__)


# index page
@main.route("/")
def home():
    return render_template("index.html")


# about page
@main.route("/about")
def about():
    return render_template("about.html")


# products page
@main.route("/products")
def products():
    return render_template("products.html")


# contact page
@main.route("/contact")
def contact():
    return render_template("contact.html")
