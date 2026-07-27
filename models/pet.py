# pet.py
from extensions import db
from .favourite import favourites

# Creation of a pet class
class Pet(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    species = db.Column(db.String(50), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(50), nullable = False)
    status = db.Column(db.String(50), nullable = False, default = "Available")
    image_url = db.Column(db.String(300), nullable = False)
    shelter_id = db.Column(db.Integer, db.ForeignKey("shelters.id"), nullable = False)
    breed = db.Column(db.String(50), nullable=False)

# One shelter has many pets
    shelter = db.relationship("Shelter", back_populates="pets")

# one pet can have many adoption requests
    adoption_requests = db.relationship("AdoptionRequest", back_populates = "pet")

# A many to many relationship with users through favourites table
    favourited_by = db.relationship("User", secondary = favourites, back_populates = "favourite_pets")