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

# A route to view all existing shelters
@shelter.route("/view-all-shelters", methods=["GET"])
def view_all_shelters():
    all_shelters = Shelter.query.all()
    return[{ "id": shelter.id, "name": shelter.name,
        "email": shelter.email, "phone": shelter.phone,
        "city": shelter.city, "address": shelter.address
    }for shelter in all_shelters
    ], 200

# A route to view one shelter
@shelter.route("/view-shelter/<int:id>", methods=["GET"])
def view_one_shelter(id):
    one_shelter = Shelter.query.filter_by(id=id).first()
    if one_shelter is None:
        return{"Error": "Shelter not found"}, 404

    return {"id": one_shelter.id, "name": one_shelter.name,
        "address": one_shelter.address, "city": one_shelter.city,
        "phone": one_shelter.phone, "email": one_shelter.email
    },200

# Route to update a shelter's details
@shelter.route("/shelter/<int:id>", methods=["PATCH"])
@jwt_required()
def update_shelter(id):

    access_right = get_jwt()
    role = access_right["role"]

    if role != "admin":
        return {"Error":"You do not have admin rights" },403

    shelter_to_update = Shelter.query.filter_by(id=id).first()
    if shelter_to_update is None:
        return { "Error":"Shelter not found"},404
    data = request.get_json()

# validations to ensure an admin can edit a particular field as well as checking whether the given field has a value
    if "name" in data:
        if data["name"].strip() == "":
            return {"Error": "Shelter name cannot be empty"}, 400
        shelter_to_update.name = data["name"]
    if "address" in data:
        if data["address"].strip() == "":
            return {"Error": "Shelter address cannot be empty"}, 400
        shelter_to_update.address = data["address"]
    if "city" in data:
        if data["city"].strip() == "":
            return {"Error": "Shelter city cannot be empty"}, 400
        shelter_to_update.city = data["city"]
    if "phone" in data:
        if data["phone"].strip() == "":
            return {"Error": "Shelter phone number cannot be empty"}, 400
        shelter_to_update.phone = data["phone"]
    if "email" in data:
        if data["email"].strip() == "":
            return {"Error": "Shelter email cannot be empty"}, 400
        existing_email = Shelter.query.filter_by(email=data["email"]).first()
        
    # shelter keeps existing email
    if existing_email and existing_email.id != shelter_to_update.id:
        return {"Error": "Another shelter already uses this email."}, 400
    shelter_to_update.email = data["email"]

    db.session.commit()
    return {
        "message":"Shelter updated successfully",
        "shelter_id": shelter_to_update.id,
        "name": shelter_to_update.name
    },200

@shelter.route("/shelter/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_shelter(id):

    access_right = get_jwt()
    role = access_right["role"]

    if role != "admin":
        return {"Error":"You do not have admin rights"},403

    shelter_to_delete = Shelter.query.filter_by(id=id).first()
    if shelter_to_delete is None:
        return {"Error":"Shelter not found"},404

    if shelter_to_delete.pets:
        return {"Error":"Cannot delete shelter because it has pets assigned"},400

    db.session.delete(shelter_to_delete)
    db.session.commit()

    return {
        "message":"Shelter deleted successfully"
    },200
    