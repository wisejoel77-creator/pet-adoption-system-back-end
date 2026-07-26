# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)
bcrypt = Bcrypt(app)

# Set up '/' route
@app.route("/")
def home():
    return {"message": "Pawfound API running"}


if __name__ == "__main__":
    app.run(debug=True)
