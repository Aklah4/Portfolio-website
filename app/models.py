from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import login_manager


class AdminUser(UserMixin):
    def __init__(self, doc):
        self.id = str(doc["_id"])
        self.username = doc["username"]
        self.email = doc["email"]
        self.password_hash = doc["password_hash"]

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    from flask import current_app
    from bson import ObjectId
    try:
        doc = current_app.mongo["admin_users"].find_one({"_id": ObjectId(user_id)})
        if doc:
            return AdminUser(doc)
    except Exception:
        pass
    return None
