from flask import Blueprint, app

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")



from . import routes