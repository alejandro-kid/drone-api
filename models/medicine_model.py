import json

from db_config  import db


class Medication(db.Model):
    __tablename__ = 'medication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    code = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(100), nullable=False)

    drone_id = db.Column(db.String(100), db.ForeignKey('drone.id'))

    def __init__(self, name, weight=None, code=None, image=None):
        self.name = name
        self.weight = weight
        self.code = code
        self.image = image

    def __repr__(self):
        location_object = {
            'name': self.name,
            'weight': self.weight,
            'code': self.code,
            'image': self.image
        }
        return json.dumps(location_object)