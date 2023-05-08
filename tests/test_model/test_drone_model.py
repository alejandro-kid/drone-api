from models.drone_model import Drone
from tests.conftest import medicaments


def test_add_a_medication(app):
    with app.app_context():
        drone = Drone.query.filter_by(serial_number="LNVotKpL0QmcHjvwJeTz").first()
        stored_and_not_stored = drone.add_medication([medicaments[0]])
        assert len(stored_and_not_stored["stored"]) == 1
        assert len(stored_and_not_stored["not_stored"]) == 0
        assert stored_and_not_stored["stored"][0].name == medicaments[0]["name"]
        assert stored_and_not_stored["stored"][0].weight == medicaments[0]["weight"]
        assert stored_and_not_stored["stored"][0].code == medicaments[0]["code"]
        assert stored_and_not_stored["stored"][0].status == "LOADED"


def test_add_two_medications():
    drone = Drone.query.filter_by(
        serial_number="QF8bnGItdpWoVP7NPdS4crPS9LckPbuzidr0FvKuS8y")\
        .first()
    stored_and_not_stored = drone.add_medication(medicaments)

    assert len(stored_and_not_stored["stored"]) == 2
    assert len(stored_and_not_stored["not_stored"]) == 1

    assert stored_and_not_stored["stored"][0].name == medicaments[0]["name"]
    assert stored_and_not_stored["stored"][0].weight == medicaments[0]["weight"]
    assert stored_and_not_stored["stored"][0].code == medicaments[0]["code"]
    assert stored_and_not_stored["stored"][0].status == "LOADED"

    assert stored_and_not_stored["stored"][1].name == medicaments[2]["name"]
    assert stored_and_not_stored["stored"][1].weight == medicaments[2]["weight"]
    assert stored_and_not_stored["stored"][1].code == medicaments[2]["code"]
    assert stored_and_not_stored["stored"][1].status == "LOADED"

    assert stored_and_not_stored["not_stored"][0]["name"] == medicaments[1]["name"]
    assert stored_and_not_stored["not_stored"][0]["weight"] == \
                                                    medicaments[1]["weight"]
    assert stored_and_not_stored["not_stored"][0]["code"] == medicaments[1]["code"]

def test_add_cero_medications():
    drone = Drone.query.filter_by(
        serial_number="HTU8L8SO2Xx3EYmkKAz4iuFBY2gAo")\
        .first()
    stored_and_not_stored = drone.add_medication([medicaments[3]])

    assert len(stored_and_not_stored["stored"]) == 0
    assert len(stored_and_not_stored["not_stored"]) == 1

    assert stored_and_not_stored["not_stored"][0]["name"] == medicaments[3]["name"]
    assert stored_and_not_stored["not_stored"][0]["weight"] == \
                                                    medicaments[3]["weight"]
    assert stored_and_not_stored["not_stored"][0]["code"] == medicaments[3]["code"]
