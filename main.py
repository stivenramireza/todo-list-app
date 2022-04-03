import unittest

from flask import (
    request,
    make_response,
    redirect,
    render_template,
    session,
    flash,
    url_for,
)
from flask_login import login_required, current_user

from src.app import create_app
from src.firestore_service import add_todo, get_todos, delete_todo, update_todo
from src.forms import TodoForm, DeleteTodoForm, UpdateTodoForm

app = create_app()


@app.route("/")
def index() -> object:
    user_ip = request.remote_addr
    response = make_response(redirect("/hello"))
    session["user_ip"] = user_ip
    return response


@app.route("/hello", methods=["GET", "POST"])
@login_required
def hello() -> object:
    user_ip = session.get("user_ip")
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()

    context = {
        "user_ip": user_ip,
        "todos": get_todos(user_id=username),
        "username": username,
        "todo_form": todo_form,
        "delete_form": delete_form,
        "update_form": update_form,
    }

    if todo_form.validate_on_submit():
        add_todo(user_id=username, description=todo_form.description.data)
        flash("Add has been created successfully")
        return redirect(url_for("hello"))

    return render_template("hello.html", **context)


@app.route("/todos/delete/<string:todo_id>", methods=["GET", "POST"])
def delete(todo_id: str) -> object:
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)
    return redirect(url_for("hello"))


@app.route("/todos/update/<string:todo_id>/<int:done>", methods=["GET", "POST"])
def update(todo_id: str, done: bool) -> object:
    user_id = current_user.id
    update_todo(user_id=user_id, todo_id=todo_id, done=done)
    return redirect(url_for("hello"))


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
