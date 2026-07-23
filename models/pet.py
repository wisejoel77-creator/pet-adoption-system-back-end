# pet.py
from app import db

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
    shelter_id = db.Column(db.Integer, db.ForeignKey("shelters.id"), required = True)
    breed = db.Column(db.String(50), nullable=False)

    shelter = db.relationship("Shelter", back_populates = "pets")
