# Adoption_request.py file
from app import db
from datetime import datetime

# Adoption request class
class AdoptionRequest(db.Model):
    __tablename__ = "adoption_requests"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable = False)
    status = db.Column(db.String, nullable = False, default = "Pending")
    request_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    notes = db.Column(db.Text, nullable = True)

# Link users and pets through an adoption request object

    user = db.relationship("User", back_populates = "adoption_requests")
    pet = db.relationship("Pet", back_populates = "adoption_requests")