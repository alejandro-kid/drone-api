import json
from db_config import db
from models.medicine_model import Medication


class Drone(db.Model):
    __tablename__ = 'drone'

    serial_number = db.Column(db.String(100), primary_key=True, unique=True, \
        nullable=False)
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

    @staticmethod
    def register_drone(serial_number, model, battery_capacity=100, \
             state='IDLE'):
        new_drone = Drone(serial_number, model, battery_capacity)
        db.session.add(new_drone)
        db.session.commit()


    def __repr__(self):
        location_object = {
            'serial_number': self.serial_number,
            'model': self.model,
            'weight_limit': str(self.weight_limit) + ' g',
            'battery_capacity': str(self.battery_capacity) + ' %',
            'state': self.state
        }
        return json.dumps(location_object)


    def add_medication(self, medications: list) -> object:

        stored_and_not_stored = {
            "stored": [],
            "not_stored": []
        }
        commit = False

        if self.state == 'LOADING' or self.state == 'IDLE':
            loaded_medications = Medication.query.filter_by(
                drone_id=self.serial_number
                ).all()
            weight_space = self.weight_limit - \
                sum([medication.weight for medication in loaded_medications])

            if weight_space > 0:
                for medication in medications:
                    if weight_space >= medication["weight"]:
                        weight_space -= medication["weight"]
                        medication = Medication(medication["name"],
                            medication["weight"], medication["code"],
                            'LOADED', self.serial_number)
                        db.session.add(medication)
                        stored_and_not_stored["stored"].append(medication)
                        commit = True
                    else:
                        stored_and_not_stored["not_stored"].append(medication)

                    if weight_space == 0:
                        break
            else:
                stored_and_not_stored["not_stored"].extend(medications)

            if commit:
                if self.state == 'IDLE':
                    Drone.query.filter_by(serial_number=self.serial_number).\
                        update({'state': 'LOADING'})
                db.session.commit()

        return stored_and_not_stored

