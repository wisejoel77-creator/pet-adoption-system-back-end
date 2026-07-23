# Shelter.py
from app import db

# Define a shelter class
class Shelter(db.Model):
    __tablename__ = "shelters"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    address = db.Column(db.String(50), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(20), nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False, unique = True)