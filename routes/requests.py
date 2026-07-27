from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.adoption_request import AdoptionRequest
from extensions import db

adoptionRequests = Blueprint("adoptionRequests",__name__ )

# adoption requests route
@adoptionRequests.route("/adoption-request", methods=["POST"])
@jwt_required()
def create_adoption_request():
    data = request.get_json()

    current_user_id = get_jwt_identity()
    pet_id = data.get("pet_id")
    notes = data.get("notes")

    if pet_id is None:
        return{"Error": "Pet id cannot be empty"}, 400

# Create a new Adoption request instance
    new_request = AdoptionRequest(
        user_id = current_user_id,
        pet_id = pet_id, 
        notes = notes
    )
    db.session.add(new_request)
    db.session.commit()

    return{
        "message": " A new adoption request has been submitted",
        "request_id": new_request.id
    },201