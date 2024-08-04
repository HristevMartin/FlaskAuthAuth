import os
from datetime import datetime, timedelta

import jwt
from bson import ObjectId
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import BadRequest

from db_extensions import mongo

jwt_secret_key = os.getenv("SECRET_KEY")

class AuthManager:
    @staticmethod
    def encode_token(user_id, role):
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(days=7),
            "role": role,
        }
        token = jwt.encode(payload, key=jwt_secret_key, algorithm="HS256")
        return token

    @staticmethod
    def decode_token(token):
        try:
            data = jwt.decode(token, key=jwt_secret_key, algorithms=["HS256"])
            return data["sub"], data["role"]

        except jwt.ExpiredSignatureError:
            raise BadRequest("Token expired")

        except jwt.InvalidTokenError:
            raise BadRequest("Invalid token")


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    user_id, role = AuthManager.decode_token(token)

    if mongo.db.blacklisted_tokens.find_one({"token": token}):
        return None

    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    except Exception as e:
        print("Failed to fetch user from MongoDB:", str(e))
        return None

    return user
