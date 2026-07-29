# Config.py
import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///pawfound.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
