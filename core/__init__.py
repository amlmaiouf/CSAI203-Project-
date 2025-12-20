from flask import Flask
from config.config import config_by_name
from core.db_singelton import db

def create_app(config_name='development'):
    """
    App Factory
    """
    # Initialize Flask
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')

    # Load Config
    app.config.from_object(config_by_name[config_name])

    # Initialize Database Singleton
    db.init_app(app)

    # Register Blueprints (We will update the import path shortly)
    from controllers.main_controller import main_controller
    app.register_blueprint(main_controller)

    return app