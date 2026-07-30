from flask import Flask
import os
from config import config_map
from app.extentions import db, migrate, oauth, login_manager


# create app function which builds everything and connects all
def create_app(test_config=None):
    # flask instance which is our app
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config_map[env])
    # starting all instances imported in app
    db.init_app(app)
    migrate.init_app(app, db)
    oauth.init_app(app)
    login_manager.init_app(app)
    # set the login view ; the route for people when they need to log in
    login_manager.login_view = "auth.login"
    # registering oauth config to link between google and oauth: name client id client secret server url and client args
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
    from app import models
    from app.routes.main import main
    from app.routes.auth import auth

    # saving blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app
