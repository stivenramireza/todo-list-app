from flask import render_template, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user

from src.auth.app import auth
from src.forms import LoginForm
from src.firestore_service import get_user
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

            if password == password_from_db:
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


@auth.route("/logout")
@login_required
def logout() -> object:
    logout_user()
    flash("See you soon!")
    return redirect(url_for("auth.login"))
