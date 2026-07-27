from flask import Blueprint, request 
from models.user import User
auth = Blueprint ("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    role = data.get("role")
    password = data.get("password")

    if username is None or username.strip() == "":
        return ("username must be filled in")

    existing_user = User.query.filter_by(email=email).first()
    
    