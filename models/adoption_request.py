# Adoption_request.py file
from app import db

# Adoption request class
class AdoptionRequest(db.Model):
    __tablename__ = "adoption_requests"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable = False)
    status = db.Column(db.String, nullable = False, default = "Pending")
    request_date = db.Column(db.DateTime, nullable = False)
    notes = db.Column(db.Text, nullable = True)

# Set a many to many relationship between pets and users using Adoption_Requests table
    user = db.relationship("User", back_populates = "adoption_requests")
    pet = db.relationship("Pet", back_populates = "adoption_requests")