from extensions import db
from flask_jwt_extended import jwt_required, get_jwt
from flask import Blueprint, request

shelter = Blueprint("shelter", __name__)

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