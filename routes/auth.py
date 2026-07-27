# imports
from flask import Blueprint, request 
from models.user import User
from extensions import bcrypt, db
from flask_jwt_extended import create_access_token
auth = Blueprint ("auth", __name__)

#register route
@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    role = data.get("role")
    password = data.get("password")

# Validations to ensure that email, username and password fields are not empty
    if username is None or username.strip() == "":
        return ("username must be filled in")
    if email is None or ("@") not in email:
     return("Invalid email format. Please put in the correct email")
    if password is None or password.strip() == "":
       return("Password field must not be empty")

# Validation to check whether the registered email already exists
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

#login route
@auth.route("/login", methods=["POST"])
def login():
# get data and unpack it
   data = request.get_json()

   email = data.get("email")
   password = data.get("password")
   login_user = User.query.filter_by(email=email).first()

   if login_user is None:
      return("User login was not successful")
   if not bcrypt.check_password_hash(login_user.password_hash, password):
    return("Wrong password. Please try again")

# Generate a token using the create_access_token function imported from flask
   token = create_access_token(
      identity=login_user.id,
      additional_claims={"role": login_user.role})

# return the access token back to the front end
   return {
    "access_token": token
}

