# imports
from flask import Blueprint, request 
from models.user import User
from extensions import bcrypt, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
auth = Blueprint ("auth", __name__)

#register route
@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    role = data.get("adopter")
    password = data.get("password")

# Validations to ensure that email, username and password fields are not empty
    if username is None or username.strip() == "":
        return {"Error": "username must be filled in"}, 400
    if email is None or ("@") not in email or "." not in email:
     return{"Error" : "Invalid email format. Please put in the correct email"}, 400
    if password is None or password.strip() == "":
       return{"Error": "Password field must not be empty"}, 400

# Validation to check whether the registered email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None:
        return {"Error": "A user with this email already exists. Use a different email"}, 409

    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        return {"Error": "Username already exists"}, 409

    hashed_password = bcrypt.generate_password_hash(password)
    password_hash = hashed_password.decode("utf-8")

    new_user = User(username = username, email = email, role = role, password_hash = password_hash)
    db.session.add(new_user)
    db.session.commit()

    return{
       "message": "User created successfully",
       "user_name": username
    }, 201

#login route
@auth.route("/login", methods=["POST"])
def login():
# get data and unpack it
   data = request.get_json()

   email = data.get("email")
   password = data.get("password")
   login_user = User.query.filter_by(email=email).first()

   if login_user is None:
      return{"Error": "User login was not successful"}, 401
   if not bcrypt.check_password_hash(login_user.password_hash, password):
    return{"Error": "Wrong password. Please try again"}, 401

# Generate a token using the create_access_token function imported from flask
   token = create_access_token(
      identity=str(login_user.id),
      additional_claims={"role": login_user.role})

# return the access token back to the front end
   return {"access_token": token}

# route to verify a user's identity
@auth.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user is None:
        return {"Error": "User not found"},404
    return {"user_id": current_user_id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "message": "You are authenticated"
    }, 200


