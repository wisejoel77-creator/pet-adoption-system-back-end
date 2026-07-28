from extensions import db
from flask_jwt_extended import jwt_required, get_jwt
from flask import Blueprint, request
from models.shelter import Shelter

shelter = Blueprint("shelter", __name__)

# A route that enables an administrator to add a new shelter
@shelter.route("/add-shelter", methods=["POST"])
@jwt_required()
def add_shelter():
    access_right = get_jwt()
    role = access_right["role"]

    if role != "admin":
        return{"Error": "You do not have the admin rights to access this page"}, 403
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")

    # validations to ensure none of the above fields are empty
    if name is None or name.strip() == "":
        return{"Error": "Name of a shelter must be provided. Please fill out this field"}
    if email is None or email.strip() == "":
        return{"Error": "The shelter's email must be provided. Please fill out this field"}
    if address is None or address.strip() == "":
        return{"Error": "The shelter's address must be provided. Please fill out this field"}
    if city is None or city.strip() == "":
        return{"Error": "The city that the shelter is located must be provided. Please fill out this field"}
    if phone is None or phone.strip() == "":
        return{"Error": "The shelter's phone number must be provided. Please fill out this field"}

# validation to check whether the shelter email and phone number already exists
    existing_email = Shelter.query.filter_by(email=email).first()
    if existing_email is not None:
        return {"Error": "A shelter with this email already exists. Please try again with a different email."}, 400

    existing_phone_number = Shelter.query.filter_by(phone=phone).first()
    if existing_phone_number is not None:
        return{"Error": "A shelter with this phone number already exists. Please try again with a different phone number."}, 400

# new shelter instance
    new_shelter = Shelter( name = name, address = address,
        email = email, phone = phone, city = city)

# Save changes to the database
    db.session.add(new_shelter)
    db.session.commit()

    return { "message": "A new shelter has been created successfully",
    "shelter_id": new_shelter.id,
    "name": new_shelter.name }, 201
    