import firebase_admin
from firebase_admin import credentials, firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()


def get_users() -> object:
    return db.collection("users").get()


def get_user(user_id: str) -> object:
    return db.collection("users").document(user_id).get()


def add_user(user_data: object) -> None:
    user_ref = db.collection("users").document(user_data.username)
    user_ref.set({"password": user_data.password})


def get_todos(user_id: str) -> object:
    return db.collection("users").document(user_id).collection("todos").get()


def add_todo(user_id: str, description: str) -> None:
    todos_collection_ref = db.collection("users").document(user_id).collection("todos")
    todos_collection_ref.add({"description": description, "done": False})


def _get_todo_ref(user_id: str, todo_id: str) -> object:
    return db.document("users/{}/todos/{}".format(user_id, todo_id))


def delete_todo(user_id: str, todo_id: str) -> None:
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()


def update_todo(user_id: str, todo_id: str, done: bool) -> None:
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_done = not bool(done)
    todo_ref.update({"done": todo_done})
