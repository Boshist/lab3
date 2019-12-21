import os
from config import db
from models import Pet

# Data to initialize database with
PETS = [
    {"pet_name": "Perry", "pet_species": "Parrot", "pet_price": 14},
    {"pet_name": "Bob", "pet_species": "Fish", "pet_price": 2},
    {"pet_name": "Daisy", "pet_species": "Dog", "pet_price": 20},
    {"pet_name": "Jack", "pet_species": "Dog", "pet_price": 27},
]

# Delete database file if it exists currently
if os.path.exists("pets.db"):
    os.remove("pets.db")

# Create the database
db.create_all()

# iterate over the PETS structure and populate the database
for pet in PETS:
    p = Pet(pet_name=pet.get("pet_name"), pet_species=pet.get("pet_species"), pet_price=pet.get("pet_price"))
    db.session.add(p)

db.session.commit()
