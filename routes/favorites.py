from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User
from models.pet import Pet

favourites = Blueprint("favourites", __name__)

# Add a pet to favourites
@favourites.route("/add-favourite", methods=["POST"])
@jwt_required()
def add_favourite():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    pet_id = data.get("pet_id")

    if pet_id is None:
        return {"error": "Pet ID is required"}, 400

    user = User.query.get(current_user_id)
    pet = Pet.query.get(pet_id)

    if pet is None:
        return {"error": "Pet not found"}, 404

    # Prevent duplicates
    if pet in user.favourite_pets:
        return {"error": "Pet is already in your favourites"}, 400

    user.favourite_pets.append(pet)
    db.session.commit()

    return {"message": "Pet added to favourites successfully"}, 201

# View favourite pets
@favourites.route("/my-favourites", methods=["GET"])
@jwt_required()
def view_favourites():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    favourites_list = []

    for pet in user.favourite_pets:
        favourites_list.append({
            "id": pet.id,
            "name": pet.name,
            "species": pet.species,
            "breed": pet.breed,
            "age": pet.age,
            "gender": pet.gender,
            "status": pet.status,
            "image_url": pet.image_url
        })

    return favourites_list, 200

# Remove a pet from favourites
@favourites.route("/remove-favourite/<int:pet_id>", methods=["DELETE"])
@jwt_required()
def remove_favourite(pet_id):
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)
    pet = Pet.query.get(pet_id)

    if pet is None:
        return {"error": "Pet not found"}, 404

    if pet not in user.favourite_pets:
        return {"error": "Pet is not in your favourites"}, 404

    user.favourite_pets.remove(pet)
    db.session.commit()

    return {"message": "Pet removed from favourites successfully"}, 200
