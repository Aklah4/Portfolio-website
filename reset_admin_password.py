import os
from dotenv import load_dotenv
load_dotenv(override=True)
from werkzeug.security import generate_password_hash
from app import create_app

app = create_app()

with app.app_context():
    admin_col = app.mongo["admin_users"]
    admin_doc = admin_col.find_one({"username": "admin"})
    if admin_doc:
        admin_col.update_one(
            {"username": "admin"},
            {"$set": {"password_hash": generate_password_hash(os.environ["ADMIN_PASSWORD"])}},
        )
        print("Admin password updated successfully.")
    else:
        print("No admin user found. Run seed.py first.")
