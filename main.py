from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from config import DevApplication
from db_extensions import mongo
from resources.routes import routes


def create_app(config_class=DevApplication):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize MongoDB
    mongo.init_app(app)

    # Setup the API using Flask-Restful
    api = Api(app)

    # Register API routes
    [api.add_resource(*r) for r in routes]

    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
