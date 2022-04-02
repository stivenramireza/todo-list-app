import unittest

from flask import request, make_response, redirect, render_template, session
from flask_login import login_required

from src.app import create_app
from src.firestore_service import get_users, get_todos

app = create_app()


@app.route("/")
def index() -> object:
    user_ip = request.remote_addr
    response = make_response(redirect("/hello"))
    session["user_ip"] = user_ip
    return response


@app.route("/hello")
@login_required
def hello() -> object:
    user_ip = session.get("user_ip")
    username = session.get("username")

    context = {
        "user_ip": user_ip,
        "todos": get_todos(user_id=username),
        "username": username,
    }

    return render_template("hello.html", **context)


@app.errorhandler(404)
def not_found(error: object) -> object:
    return render_template("404.html", error=error)


@app.errorhandler(500)
def internal_server_error(error: object) -> object:
    return render_template("500.html", error=error)


@app.cli.command()
def test() -> None:
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)
