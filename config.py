import os
import connexion

# create an application instance

drone_api = connexion.App(__name__, specification_dir='./swagger')

drone_api.add_api('swagger.yml')
