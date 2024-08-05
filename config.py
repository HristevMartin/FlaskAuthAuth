# config.py
import os

class Config:
    DEBUG = True
    TESTING = True
    MONGODB_SETTINGS = {
        'db': os.getenv('MONGO_DB', 'travelDB'),
        'host': os.getenv('MONGO_HOST', 'localhost'),
        'port': int(os.getenv('MONGO_PORT', 27017))
    }
