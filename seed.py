import os
from dotenv import load_dotenv
load_dotenv(override=True)
from app import create_app
from app.db import db
from app.models import AdminUser

app = create_app()

with app.app_context():
    db.create_all()

    if not AdminUser.query.filter_by(username="admin").first():
        admin = AdminUser(username="admin", email="admin@example.com")
        admin.set_password(os.environ["ADMIN_PASSWORD"])
        db.session.add(admin)
        db.session.commit()
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
