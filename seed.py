from app import app
from extensions import db, bcrypt

from models.user import User
from models.shelter import Shelter
from models.pet import Pet

with app.app_context():
    print("Deleting old data...")

    Pet.query.delete()
    Shelter.query.delete()
    User.query.delete()

    db.session.commit()
    print("Creating users...")

    admin = User(username="admin", email="admin@pawfound.com",
        role="admin",
        password_hash=bcrypt.generate_password_hash("admin123").decode("utf-8")
    )

    user1 = User( username="joel",email="joel@example.com", role="adopter",
        password_hash=bcrypt.generate_password_hash("password123").decode("utf-8")
    )

    user2 = User(username="mary",email="mary@example.com",role="adopter",
        password_hash=bcrypt.generate_password_hash("password123").decode("utf-8")
    )

    db.session.add_all([admin, user1, user2])
    db.session.commit()
    print("Creating shelters...")

    shelter1 = Shelter( name="Happy Paws Shelter", address="123 Main Street",
        city="Nairobi",phone="0711111111",
        email="happy@pawfound.com"
    )

    shelter2 = Shelter(name="Safe Haven", address="45 Westlands Road",
        city="Nairobi", phone="0722222222",
        email="safe@pawfound.com"
    )

    shelter3 = Shelter(name="Pet Rescue Kenya", address="10 Mombasa Road",
        city="Nairobi", phone="0733333333",
        email="rescue@pawfound.com"
    )

    db.session.add_all([shelter1, shelter2, shelter3])
    db.session.commit()
    print("Creating pets...")

    pets = [
        Pet(name="Bella", species="Dog", breed="German Shepherd",
            age=2, gender="female",
            image_url="https://images.unsplash.com/photo-1517849845537-4d257902454a",
            shelter_id=shelter1.id
        ),
        Pet(name="Max",species="Dog", breed="Golden Retriever",
            age=3, gender="male",
            image_url="https://images.unsplash.com/photo-1558788353-f76d92427f16",
            shelter_id=shelter1.id
        ),
        Pet(name="Luna", species="Cat", breed="Persian",
            age=1, gender="female",
            image_url="https://images.unsplash.com/photo-1519052537078-e6302a4968d4",
            shelter_id=shelter2.id
        ),
        Pet(name="Charlie", species="Dog", breed="Labrador",
            age=4, gender="male",
            image_url="https://images.unsplash.com/photo-1518717758536-85ae29035b6d",
            shelter_id=shelter2.id
        ),
        Pet(name="Milo", species="Cat", breed="Siamese",
            age=2, gender="male",
            image_url="https://images.unsplash.com/photo-1574158622682-e40e69881006",
            shelter_id=shelter3.id
        )
    ]

    db.session.add_all(pets)
    db.session.commit()

    print("Database seeded successfully!")