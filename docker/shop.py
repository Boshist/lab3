"""
This is the pets module and supports all the REST actions for the
pets data
"""

from flask import make_response, abort
from config import db
from models import Pet, PetSchema


def read_all():
    """
    This function responds to a request for /api/shop
    with the complete lists of pets
    :return:        json string of list of pets
    """
    # Create the list of pets from our data
    pets = Pet.query.order_by(Pet.pet_name).all()

    # Serialize the data for the response
    pet_schema = PetSchema(many=True)
    data = pet_schema.dump(pets)
    return data


def read_one(pet_id):
    """
    This function responds to a request for /api/shop/{pet_id}
    with one matching pet from shop
    :param pet_id:   Id of pet to find
    :return:            pet matching id
    """
    # Get the pet requested
    pet = Pet.query.filter(Pet.pet_id == pet_id).one_or_none()

    # Did we find a pet?
    if pet is not None:

        # Serialize the data for the response
        pet_schema = PetSchema()
        data = pet_schema.dump(pet)
        return data

    # Otherwise didn't find that pet
    else:
        abort(
            404,
            "Pet with Id: {pet_id} was not found".format(pet_id=pet_id),
        )


def create(pet):
    """
    This function creates a new pet in the shop structure
    based on the passed in pet data
    :param pet:  pet to create in shop structure
    :return:        201 on success, 406 on existing pet
    """
    pet_name = pet.get("pet_name")
    pet_species = pet.get("pet_species")
    pet_price = pet.get("pet_price")

    existing_pet = (
        Pet.query.filter(Pet.pet_name == pet_name)
        .filter(Pet.pet_species == pet_species)
        .filter(Pet.pet_price == pet_price)
        .one_or_none()
    )

    # Can we insert this pet?
    if existing_pet is None:

        # Create a pet instance using the schema and the passed in pet
        schema = PetSchema()
        new_pet = schema.load(pet, session=db.session)

        # Add the pet to the database
        db.session.add(new_pet)
        db.session.commit()

        # Serialize and return the newly created pet in the response
        data = schema.dump(new_pet)

        return data, 201

    # Otherwise pet already exists
    else:
        abort(
            409,
            "Pet {pet_name} of {pet_species} species with the price {pet_price} already exists".format(
                pet_name=pet_name, pet_species=pet_species, pet_price=pet_price
            ),
        )


def update(pet_id, pet):
    """
    This function updates an existing pet in the shop
    Throws an error if a pet with the same values we want to update to
    already exists in the database.
    :param pet_id:   Id of the pet to update
    :param pet:      pet to update
    :return:            updated shop
    """
    # Get the pet requested from the db into session
    update_pet = Pet.query.filter(
        Pet.pet_id == pet_id
    ).one_or_none()

    # Try to find an existing pet with the same values as the update
    pet_name = pet.get("pet_name")
    pet_species = pet.get("pet_species")
    pet_price = pet.get("pet_price")

    existing_pet = (
        Pet.query.filter(Pet.pet_name == pet_name)
        .filter(Pet.pet_species == pet_species)
        .filter(Pet.pet_price == pet_price)
        .one_or_none()
    )

    # If our pet does not exist
    if update_pet is None:
        abort(
            404,
            "Pet was not found for Id: {pet_id}".format(pet_id=pet_id),
        )

    # Or update creates a duplicate
    elif (
        existing_pet is not None and existing_pet.pet_id != pet_id
    ):
        abort(
            409,
            "Pet {pet_name} of {pet_species} species with the price {pet_price} already exists".format(
                pet_name=pet_name, pet_species=pet_species, pet_price=pet_price
            ),
        )

    # Otherwise update
    else:

        # turn the passed in pet into a db object
        schema = PetSchema()
        update = schema.load(pet, session=db.session)

        # Set the id to the pet we want to update
        update.pet_id = update_pet.pet_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated pet in the response
        data = schema.dump(update_pet)

        return data, 200


def delete(pet_id):
    """
    This function deletes a pet from the shop
    :param pet_id:   Id of the pet to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the pet requested
    pet = Pet.query.filter(Pet.pet_id == pet_id).one_or_none()

    # Pet exists
    if pet is not None:
        db.session.delete(pet)
        db.session.commit()
        return make_response(
            "Pet with id {pet_id} was successfully deleted".format(pet_id=pet_id), 200
        )

    # Otherwise
    else:
        abort(
            404,
            "Pet with id: {person_id} does not exist".format(pet_id=pet_id),
        )
