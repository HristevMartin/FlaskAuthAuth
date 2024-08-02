from datetime import datetime, timedelta

import jwt
from bson import ObjectId
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import BadRequest

# from app import db
# from db_models.token import Token


class AuthManager:
    @staticmethod
    def encode_token(user_id, role):
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(days=1),
            "role": role
        }
        token = jwt.encode(payload, key='verysecrettoken', algorithm="HS256")
        return token

    @staticmethod
    def decode_token(token):
        try:
            data = jwt.decode(token, key='verysecrettoken', algorithms=["HS256"])
            return data["sub"], data["role"]

        except jwt.ExpiredSignatureError:
            raise BadRequest("Token expired")

        except jwt.InvalidTokenError:
            raise BadRequest("Invalid token")

    @staticmethod
    def encode_password_reset_token(user, expires_sec=1800):
        payload = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(seconds=expires_sec),
        }
        token = jwt.encode(payload, key='verysecrettoken', algorithm="HS256")
        return token

    @staticmethod
    def decode_password_reset_token(token):
        try:
            data = jwt.decode(token, key='verysecrettoken', algorithms=["HS256"])
            return data["sub"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    # @staticmethod
    # def save_token_to_db(token, user, payload):
    #     new_token = Token(
    #         token=token,
    #         user_id=user.id,
    #         role=user.__class__.__name__,
    #         expiration_time=payload["exp"]
    #     )
    #     db.session.add(new_token)
    #     db.session.commit()
    #     try:
    #         db.session.commit()
    #     except Exception as e:
    #         db.session.rollback()
    #         print('Failed to save token:', str(e))


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    from db_extensions import mongo

    user_id, role = AuthManager.decode_token(token)

    # token_entry = Token.query.filter_by(token=token).first()
    # if token_entry is None:
    #     return None

    # check if the token has expired
    # if token_entry.expiration_time < datetime.utcnow():
    #     return None

    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    except Exception as e:
        print('Failed to fetch user from MongoDB:', str(e))
        return None

    return user
#