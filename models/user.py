# user.py file
from extensions import db
from .favourite import favourites
from datetime import datetime

# Create User class
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    email = db.Column(db.String(80), nullable = False, unique = True)
    role = db.Column(db.String(30), nullable = False, default = "adopter")
    password_hash = db.Column(db.String(100), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

 # One user can create many adoption requests
    adoption_requests = db.relationship("AdoptionRequest", back_populates = "user")

    favourite_pets = db.relationship("Pet", secondary = favourites, back_populates = "favourited_by")
