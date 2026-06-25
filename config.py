from dotenv import load_dotenv
import os

# setting the function to read from the .env file
load_dotenv()

# the config class which will contain most of settings
class Config:
    # variables read from the env file
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    
# the class for developement
class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
# the class for production
class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True