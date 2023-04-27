import connexion
import os


drone_api = connexion.App(__name__, specification_dir='./swagger')

drone_api.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                            os.path.join(drone_api.root_path, 'database/drone_db.db')

drone_api.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

drone_api.add_api('swagger.yml')
