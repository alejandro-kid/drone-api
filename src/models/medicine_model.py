import json

from src.extensions import db


class Medication(db.Model):
    __tablename__ = 'medication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    code = db.Column(db.String, unique=True, nullable=False)
    state = db.Column(db.String, db.CheckConstraint("state IN ('LOADED', \
        'DELIVERING', 'DELIVERED')"), nullable=False)
    drone_id = db.Column(db.String(100), db.ForeignKey('drone.serial_number'))

    def __init__(self, name, weight=None, code=None, state='LOADED', \
        drone_id=None):
        self.name = name
        self.weight = weight
        self.code = code
        self.state = state
        self.drone_id = drone_id

    def __repr__(self):
        location_object = {
            'name': self.name,
            'weight': self.weight,
            'code': self.code,
            'state': self.state
        }
        return json.dumps(location_object)

    @staticmethod
    def update_all_state(serial_number:str, state:str)->None:
        db.session.query(Medication).filter(Medication.drone_id == serial_number).\
            update({Medication.state: state}, synchronize_session=False)

        db.session.commit()
