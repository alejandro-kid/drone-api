import json
from db_config import db


class Drone(db.Model):
    __tablename__ = 'drone'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    model = db.Column(db.String(20), db.CheckConstraint("model IN ('Lightweight', \
        'Middleweight', 'Cruiserweight', 'Heavyweight')"), nullable=False)
    weight_limit = db.Column(db.Float, nullable=False)
    battery_capacity = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(20), db.CheckConstraint("state IN ('IDLE', 'LOADING', \
        'LOADED', 'DELIVERING', 'DELIVERED', 'RETURNING')"), nullable=False)
    
    medication = db.relationship('Medication', backref='drone', lazy=True)

    def __init__(self, serial_number, model, battery_capacity=100, \
             state='IDLE'):
        self.serial_number = serial_number
        self.model = model
        self.battery_capacity = battery_capacity
        self.state = state

        match model:
            case 'Lightweight':
                self.weight_limit = 200
            case 'Middleweight':
                self.weight_limit = 300
            case 'Cruiserweight':
                self.weight_limit = 400
            case 'Heavyweight':
                self.weight_limit = 500
            case _:
                self.weight_limit = 0

    
    def register_drone(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        location_object = {
            'id': self.id,
            'serial_number': self.serial_number,
            'model': self.model,
            'weight_limit': str(self.weight_limit) + ' g',
            'battery_capacity': str(self.battery_capacity) + ' %',
            'state': self.state
        }
        return json.dumps(location_object)