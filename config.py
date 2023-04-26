import connexion

from DBConfig import DBConfig

# create an application instance

drone_api = connexion.App(__name__, specification_dir='./swagger')

db_configuration = DBConfig()

drone_api.app.config['SQLALCHEMY_DATABASE_URI'] = db_configuration.get_uri()

drone_api.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

drone_api.add_api('swagger.yml')
