import connexion

from src.extensions import bcrypt, db


def create_app(settings_override=None):
    """
    Create a Connexion application using the app factory pattern.

    :param settings_override: Override settings
    :return: Connexion app
    """

    api = connexion.FlaskApp(__name__, specification_dir="./swagger")
    api.add_api("swagger.yml")
    api.app.config.from_object("config.settings")

    if settings_override:
        api.app.config.update(settings_override)

    extensions(api.app)

    return api.app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """

    bcrypt.init_app(app)
    db.init_app(app)

    return None
