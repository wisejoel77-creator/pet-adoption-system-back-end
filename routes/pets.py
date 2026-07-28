#pets.py
from flask_jwt_extended import jwt_required, get_jwt
from extensions import db
from flask import Blueprint, request
from models.shelter import Shelter
from models.pet import Pet
pet = Blueprint("pet", __name__)

# A route that allows an admin to create a pet
@pet.route("/add-pet", methods=["POST"])
@jwt_required()
def add_pet():
    access_right = get_jwt()
    role = access_right["role"]

    if role != "admin":
        return{"Error": "You do not have the admin rights to access this page"}, 403

    data = request.get_json()
    name = data.get("name")
    breed = data.get("breed")
    species = data.get("species")
    age = data.get("age")
    gender = data.get("gender")
    image_url = data.get("image_url")
    shelter_id = data.get("shelter_id")

    if name is None or name.strip() == "":
        return{"Error": "Name field must not be empty. Type in a pet name"}, 400
    if species is None or species.strip() == "":
        return{"Error": "Species field must contain a value. Please try again"}, 400
    if breed is None or breed.strip() == "":
        return {"Error": "Breed field must contain a value. Please type in a breed for your new pet"}, 400
    # Validate age
    if age is None:
        return {"Error": "Age field is required"}, 400
    if not isinstance(age, int):
        return {"Error": "Age must be a number"}, 400
    if age < 0:
        return {"Error": "Age cannot be negative"}, 400

# Validate gender
    if gender is None or gender.strip() == "":
        return {"Error": "Gender field is required"}, 400

    gender = gender.lower()

    if gender not in ["male", "female"]:
        return {"Error": "Gender must be either male or female"}, 400

    if image_url is None or image_url.strip() == "":
        return{"Error": "An image url has to be typed in"}, 400

    existing_shelter = Shelter.query.filter_by(id=shelter_id).first()
    if existing_shelter is None:
        return{"Error": "This shelter does not exist"}, 404

    new_pet = Pet( shelter_id = shelter_id,
        name = name,
        age = age,
        gender = gender,
        breed = breed,
        species = species,
        image_url = image_url)

    db.session.add(new_pet)
    db.session.commit()

    return{
        "message": "A new pet has been created successfully",
        "pet_id": new_pet.id,
        "name" : name
    }, 201

# Route to view all pets
@pet.route("/view-all-pets", methods=["GET"])
def view_pets():
    all_pets = Pet.query.all()
    return[{
        "name": pet.name, "species": pet.species, "breed": pet.breed,
        "age": pet.age, "gender": pet.gender, "id": pet.id,
        "status": pet.status,"image_url": pet.image_url
    }
        for pet in all_pets]

# Route to view one pet
@pet.route("/pet/<int:id>")
def get_specific_pet(id):
    one_pet = Pet.query.filter_by(id=id).first()
    if one_pet is None:
        return {"Error": "Pet not found"}, 404
    return{
        "name": one_pet.name, "species": one_pet.species, "breed": one_pet.breed,
        "age": one_pet.age, "gender": one_pet.gender, "id": one_pet.id,
        "status": one_pet.status, "image_url": one_pet.image_url
    }

# route that allows an admin to update a pet's details
@pet.route("/pet/<int:id>", methods=["PATCH"])
@jwt_required()
def update_pet(id):
    access_right = get_jwt()
    role = access_right["role"]
    if role != "admin":
        return {"Error": "You do not have the admin rights to access this page"}, 403

# validation to check whether the pet to be updated exists in the records
    pet_to_update = Pet.query.filter_by(id=id).first()
    if pet_to_update is None:
        return {"Error": "This pet does not exist. Please create a new pet or verify the pet id then try again"}, 404

    data = request.get_json()
    if "status" in data:
       pet_to_update.status = data["status"]
    if "name" in data:
        pet_to_update.name = data["name"]
    if "breed" in data:
        pet_to_update.breed = data["breed"]
    if "species" in data:
        pet_to_update.species = data["species"]
    db.session.commit()

    return {
    "message": "Pet updated successfully",
    "pet_id": pet_to_update.id,
    "status": pet_to_update.status
}

    