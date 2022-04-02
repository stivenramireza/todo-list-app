from flask import render_template, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from src.auth.app import auth
from src.forms import LoginForm
from src.firestore_service import get_user, user_post
from src.models import UserData, UserModel


@auth.route("/login", methods=["GET", "POST"])
def login() -> object:
    login_form = LoginForm()
    context = {"login_form": login_form}

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict().get("password")

            if check_password_hash(password_from_db, password):
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)
                flash("Welcome again!")
                redirect(url_for("hello"))
            else:
                flash("Invalid credentials")
        else:
            flash("User does not exist")

        return redirect(url_for("index"))

    return render_template("login.html", **context)


@auth.route("/signup", methods=["GET", "POST"])
def signup() -> object:
    signup_form = LoginForm()

    context = {"signup_form": signup_form}

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            hashed_password = generate_password_hash(password)
            user_data = UserData(username, hashed_password)
            user_post(user_data)

            user = UserModel(user_data)
            login_user(user)
            flash("Welcome!")

            return redirect(url_for("hello"))
        else:
            flash("The user already exists")

    return render_template("signup.html", **context)


@auth.route("/logout")
@login_required
def logout() -> object:
    logout_user()
    flash("See you soon!")
    return redirect(url_for("auth.login"))
