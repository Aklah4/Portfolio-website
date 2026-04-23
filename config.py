import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///app.db"
    MONGO_URI = os.environ.get("MONGO_URI")
    CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL")
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    DEBUG = False
    TESTING = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads", "projects")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
