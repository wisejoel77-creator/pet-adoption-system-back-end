# user.py file
from app import db

# Create User class
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    email = db.Column(db.String(80), nullable = False, unique = True)
    role = db.Column(db.String(30), nullable = False)
    password = db.Column(db.String(50), nullable = False)
    created_at = db.Column(db.DateTime)
