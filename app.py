# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(db, app)

@app.route("/")
def home():
    return {"message": "Pawfound API running"}


if __name__ == "__main__":
    app.run(debug=True)
