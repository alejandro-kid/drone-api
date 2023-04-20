from config import drone_api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(drone_api.app)
