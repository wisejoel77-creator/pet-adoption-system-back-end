#pets.py
from flask_jwt_extended import jwt_required, get_jwt
from extensions import db
from flask import Blueprint, request
pet = Blueprint("pet", __name__)

# A route to create a pet
@pet.route("/add-pet", methods=["POST"])
@jwt_required()
def add_pet():
    data = request.get_json()
    access_right = get_jwt()
    role = access_right["role"]

    if role != "admin":
        return{"Error": "You do not have the admin rights to access this page"}, 403
    
    name = data.get("name")
    breed = data.get("breed")
    species = data.get("species")
    age = data.get("age")
    gender = data.get("gender")


    