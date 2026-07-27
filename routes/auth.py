from flask import Blueprint, request 
from models.user import User
from extensions import bcrypt, db
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
    if email is None or ("@") not in email:
     return("Invalid email format. Please put in the correct email")
    if password is None or password.strip() == "":
       return("Password field must not be empty")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None:
        return ("Error: A user with this email already exists. Use a different email"), 409

    hashed_password = bcrypt.generate_password_hash(password)
    password_hash = hashed_password.decode("utf-8")

    new_user = User(username = username, email = email, role = role, password_hash = password_hash)
    db.session.add(new_user)
    db.session.commit()

    return{
       "message": "User created successfully",
       "user_name": username
    }
