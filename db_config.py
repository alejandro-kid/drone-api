from config import *
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(drone_api.app)
