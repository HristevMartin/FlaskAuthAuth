from flask import Flask
from config import Config
from extensions import mongo
from api import api

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)
    app.register_blueprint(api)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
