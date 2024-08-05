from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_mongoengine import MongoEngine
from config import Config
from resources.routes import routes

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    api = Api(app)

    [api.add_resource(*r) for r in routes]

    CORS(app, origins=["http://localhost:3000"])

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
