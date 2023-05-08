import connexion
import os

# create an application instance

drone_api = connexion.App(__name__, specification_dir='./swagger')

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_NAME = os.getenv("DB_NAME", "drone-api")
DB_HOST = os.getenv("DB_HOST", "localhost")

# configuration
drone_api.app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://" + f"{DB_PASS}:{DB_USER}@{DB_HOST}/{DB_NAME}"
)
drone_api.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
drone_api.add_api('swagger.yml')
