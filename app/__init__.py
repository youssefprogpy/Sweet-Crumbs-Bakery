from flask import Flask
import os
from config import DevelopmentConfig, ProductionConfig

# create app function which builds everything and connects all
def create_app(test_config = None):
    # flask instance which is our app
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV")
    if env == "development":
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)    
    from app.routes.main import main
    # saving blueprints
    app.register_blueprint(main)
    return app