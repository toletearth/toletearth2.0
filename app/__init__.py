from flask import Flask

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.models.db import close_db
    app.teardown_appcontext(close_db)

    from app.routes.main import main_bp
    from app.routes.properties import properties_bp
    from app.routes.owner import owner_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(owner_bp)

    return app
