from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager

# creating instances
db = SQLAlchemy()
migrate = Migrate()
oauth = OAuth()
login_manager = LoginManager()
