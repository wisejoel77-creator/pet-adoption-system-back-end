# favourite.py file
from extensions import db

# An association table to link pets and users that have favourited them
favourites = db.Table("favourites",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), nullable = False),
    db.Column("pet_id", db.Integer, db.ForeignKey("pets.id"), nullable = False),
    db.UniqueConstraint("user_id", "pet_id")
)