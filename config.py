import os
import connexion

# create an application instance

drone_api = connexion.App(__name__, specification_dir='./swagger')

drone_api.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_HOST",
                                                "postgresql://postgres:postgres@localhost:5432/drone_api")
drone_api.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

drone_api.add_api('swagger.yml')
