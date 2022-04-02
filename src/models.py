from flask_login import UserMixin

from src.firestore_service import get_user


class UserData:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password


class UserModel(UserMixin):
    def __init__(self, user_data: UserData) -> None:
        self.id = user_data.username
        self.password = user_data.password

    @staticmethod
    def query(user_id: str) -> object:
        user_doc = get_user(user_id)
        user_data = UserData(
            username=user_doc.id, password=user_doc.to_dict().get("password")
        )
        user_model = UserModel(user_data)
        return user_model
