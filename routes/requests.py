from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.adoption_request import AdoptionRequest
from extensions import db
from flask_jwt_extended import get_jwt
from models.pet import Pet

adoptionRequests = Blueprint("adoptionRequests",__name__ )

# A route that allows a user to create a new adoption request
@adoptionRequests.route("/adoption-request", methods=["POST"])
@jwt_required()

def create_adoption_request():
    data = request.get_json()

    claims = get_jwt()

    if claims["role"] != "adopter":
        return {"error": "Only adopters can submit requests"}, 403

    current_user_id = get_jwt_identity()
    pet_id = data.get("pet_id")
    notes = data.get("notes")

    if pet_id is None:
        return{"Error": "Pet id cannot be empty"}, 400

    # Check if pet exists
    pet = Pet.query.get(pet_id)
    if pet is None:
        return {"Error": "Pet not found"},404

    # Check pet availability
    if pet.status != "available":
        return {"Error": "This pet is not available for adoption" },400

    # Prevent duplicate requests
    existing_request = AdoptionRequest.query.filter_by( user_id=current_user_id, pet_id=pet_id ).first()
    if existing_request:
        return {"Error": "You already submitted an adoption request for this pet"},400

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

# a route to view their adoption requests
@adoptionRequests.route("/my-adoption-requests", methods=["GET"])
@jwt_required()
def get_adoption_requests():
    current_user_id = get_jwt_identity()

    requests = AdoptionRequest.query.filter_by(user_id=current_user_id).all()
    return[{
        "id": adoption_request.id,
        "pet_id": adoption_request.pet_id,
        "status": adoption_request.status,
        "notes": adoption_request.notes,
        "request_date": adoption_request.request_date.isoformat()
    } 
    for adoption_request in requests
    ], 200

# Route that allows an admin to accept or decline an adoption request
@adoptionRequests.route("/adoption-request/<int:request_id>", methods=["PATCH"])
@jwt_required()
def review_adoption_request(request_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return {"error": "Admins only"}, 403
    adoption_request = AdoptionRequest.query.get(request_id)

    if adoption_request is None:
        return {"error": "Request not found"}, 404
    
    data = request.get_json()
    status = data.get("status")

    if status not in ["Approved", "Rejected"]:
        return { "error": "Status must be Approved or Rejected" }, 400

    adoption_request.status = status

    pet = Pet.query.get(adoption_request.pet_id)
    if status == "Approved":
        pet.status = "adopted"

    db.session.commit()
    return {
    "message": "Adoption request updated successfully",
    "status": adoption_request.status
}

