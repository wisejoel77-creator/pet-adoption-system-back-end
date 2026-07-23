# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Configure my app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pawfind.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"


# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# Set up '/' route
@app.route("/")
def home():
    return {"message": "Pawfound API running"}


if __name__ == "__main__":
    app.run(debug=True)
