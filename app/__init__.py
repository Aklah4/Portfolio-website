from flask import Flask, render_template
from app.db import db, login_manager, csrf, init_mongo
from config import config


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

 
    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "admin.login"
    csrf.init_app(app)
    init_mongo(app)

    from app.blueprints.main import main_bp
    app.register_blueprint(main_bp)

    from app.blueprints.api import api_bp
    app.register_blueprint(api_bp)

    from .blueprints.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')


    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500


    with app.app_context():
        from . import models  # noqa: F401
        db.create_all()



    return app
