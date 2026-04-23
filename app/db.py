from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.uri_parser import parse_uri

login_manager = LoginManager()
csrf = CSRFProtect()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


# MongoDB setup
def init_mongo(app):
    mongo_uri = app.config.get("MONGO_URI", "mongodb://localhost:27017/portfolio")
    try:
        client = MongoClient(mongo_uri)
        client.admin.command('ping')
        db_name = parse_uri(mongo_uri).get("database") or "portfolio"
        app.mongo = client[db_name]
        print("Connected to database:", app.mongo.name)  # ← inside the function
    except ConnectionFailure:
        print("Failed to connect to MongoDB")
        app.mongo = None


