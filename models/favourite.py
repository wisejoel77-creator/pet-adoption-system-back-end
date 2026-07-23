# favourite.py file
from app import db

# An association table to link pets and users that have favourited them
favourite_table = db.Table("favourites",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("pet_id", db.Integer, db.ForeignKey("pets.id")),
    db.UniqueConstraint("user_id", "pet_id")
)