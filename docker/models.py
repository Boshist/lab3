from config import db, ma


class Pet(db.Model):
    __tablename__ = "pet"
    pet_id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(32))
    pet_species = db.Column(db.String(32))
    pet_price = db.Column(db.Integer)


class PetSchema(ma.ModelSchema):
    class Meta:
        model = Pet
        sqla_session = db.session
