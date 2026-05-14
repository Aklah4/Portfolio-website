import os
from dotenv import load_dotenv
load_dotenv(override=True)
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from app import create_app

app = create_app()

with app.app_context():
    admin_col = app.mongo["admin_users"]
    if not admin_col.find_one({"username": "admin"}):
        admin_col.insert_one({
            "username": "admin",
            "email": "admin@example.com",
            "password_hash": generate_password_hash(os.environ["ADMIN_PASSWORD"]),
            "created_at": datetime.now(timezone.utc),
        })
        print("Admin user created.")
    else:
        print("Admin user already exists, skipping.")

    projects_col = app.mongo["projects"]
    if projects_col.count_documents({}) == 0:
        projects_col.insert_one({
            "title": "Portfolio Website",
            "slug": "portfolio-website",
            "description": "A personal portfolio built with Flask, MySQL, and MongoDB.",
            "tech_stack": ["Python", "Flask", "MySQL", "MongoDB"],
            "live_url": "https://example.com",
            "github_url": "https://github.com/example/portfolio",
            "image_url": "https://via.placeholder.com/1200x675/0f172a/ede8df?text=Portfolio+Website",
            "featured": True,
        })
        print("Sample project inserted.")
    else:
        print("Projects collection already has data, skipping.")
