import json

from db_config  import db


class Medication(db.Model):
    __tablename__ = 'medication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    code = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.String, db.CheckConstraint("status IN ('LOADED', \
        'DELIVERING', 'DELIVERED')"), nullable=False)
    drone_id = db.Column(db.String(100), db.ForeignKey('drone.serial_number'))

    def __init__(self, name, weight=None, code=None, status='LOADED', \
        drone_id=None):
        self.name = name
        self.weight = weight
        self.code = code
        self.status = status
        self.drone_id = drone_id

    def __repr__(self):
        location_object = {
            'name': self.name,
            'weight': self.weight,
            'code': self.code,
            'status': self.status
        }
        return json.dumps(location_object)
