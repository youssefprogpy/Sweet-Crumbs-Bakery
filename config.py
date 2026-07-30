from dotenv import load_dotenv
import os
from pathlib import Path

# setting the function to read from the .env file
load_dotenv()

# make the dir for the .db file for sqlalchemy uri
BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
# the folder is created if not there so no potential error
INSTANCE_DIR.mkdir(exist_ok=True)
DB_PATH = INSTANCE_DIR / "sweetcrumbs.db"


# the config class which will contain most of settings
class Config:
    # variables read from the env file
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    # stopping sqlalchemy from tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# the class for developement
class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    # dev config uses computed path for db file while prd config reads from .env
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"


# the class for production
class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


# config map to guide the create_app func
config_map = {"development": DevelopmentConfig, "production": ProductionConfig}
