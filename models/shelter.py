# Shelter.py
from extensions import db

# Define a shelter class
class Shelter(db.Model):
    __tablename__ = "shelters"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    address = db.Column(db.String(250), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(20), nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False, unique = True)

 # Set a one to many relationship between shelter and pets
    pets = db.relationship("Pet", back_populates = "shelter", cascade="all, delete-orphan")