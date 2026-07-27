# imports
from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt, bcrypt

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
bcrypt.init_app(app)
CORS(app)

# Import models so Flask-Migrate can detect them
import models

# Set up '/' route
@app.route("/")
def home():
    return {"message": "Pawfound API running"}


if __name__ == "__main__":
    app.run(debug=True)
