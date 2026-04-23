from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db, login_manager


class AdminUser(UserMixin, db.Model):
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    return db.session.get(AdminUser, int(id))


class Contact(db.Model):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class PageView(db.Model):
    __tablename__ = "page_views"

    id: Mapped[int] = mapped_column(primary_key=True)
    page: Mapped[str] = mapped_column(String(255), nullable=False)
    visited_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
