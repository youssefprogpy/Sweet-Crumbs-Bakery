from flask import render_template, redirect, Blueprint, request, flash, url_for
from flask_login import login_user, logout_user, current_user, login_required
import re
from app.models import User
from app.extentions import db, oauth

auth = Blueprint("auth", __name__)

# for validating email & password
EMAIL_PATTERN = r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"


# the register route
@auth.route("/auth/register", methods=["GET", "POST"])
def register():
    # redirect already-logged-in users away from register instead of
    # letting them re-register while authenticated
    if current_user.is_authenticated:
        return redirect(url_for("main.products"))
    if request.method == "POST":
        errors = []
        name = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        # checking potential errors
        if not name or not email or not password or not confirm_password:
            flash("All Fields Required", "error")
            return redirect(url_for("auth.register"))
        if len(name) < 3:
            errors.append("Name too short")
        if not re.match(EMAIL_PATTERN, email):
            errors.append("Email Format Incorrect")
        existed = User.query.filter_by(email=email).first()
        if existed:
            errors.append("Email already used")
        if (
            len(password) < 8
            or not any(char.isdigit() for char in password)
            or not any(char in SYMBOLS for char in password)
        ):
            errors.append(
                "Password must be at least 8 characters long, include a digit and a symbol"
            )
        if password != confirm_password:
            errors.append("Passwords mismatch")
        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("auth.register"))
        user = User(name=name, email=email, password_hash=User.hashing_pass(password))
        # saving to db
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


# login route
@auth.route("/auth/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.products"))
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if not username or not password:
            flash("All fields required", "error")
            return redirect(url_for("auth.login"))
        user_in = User.query.filter_by(email=username).first()
        if (
            not user_in
            or not user_in.password_hash
            or not User.check_hash(password, user_in.password_hash)
        ):
            flash("Username or password incorrect", "error")
            return redirect(url_for("auth.login"))
        login_user(user_in)
        flash("Welcome back!", "success")
        return redirect(url_for("main.home"))
    return render_template("auth/login.html")


# logout route
@auth.route("/auth/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


# oauth google route to send users to google
@auth.route("/auth/google", methods=["GET"])
def google():
    redirect_url = url_for("auth.callback", _external=True)
    return oauth.google.authorize_redirect(redirect_url)


# oauth callback route which gets us the token for exchanging code
@auth.route("/auth/callback")
def callback():
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get("userinfo")
        if not user_info:
            flash("Google login failed. Please try again.", "error")
            return redirect(url_for("auth.login"))
        name = user_info["name"]
        email = user_info["email"]
        user_in = User.query.filter_by(email=email).first()
        if not user_in:
            user = User(name=name, email=email, oauth_provider="google")
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for("main.products"))
        if not user_in.password_hash:
            login_user(user_in)
            flash("Welcome back!", "success")
            return redirect(url_for("main.products"))
        else:
            flash(
                "This email already registered. Please log in with your password",
                "error",
            )
            return redirect(url_for("auth.login"))
    except Exception as e:
        print(f" OAuth Error: {type(e).__name__}: {e}")
        flash("Something went wrong during Google login. Please try again.", "error")
        return redirect(url_for("auth.login"))
