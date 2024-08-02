from flask import Flask
from flask_restful import Api
# from flask_cors import CORS
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

    # Enable CORS if needed
    # CORS(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
