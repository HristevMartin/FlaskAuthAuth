from datetime import datetime

from bson import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash

from managers.auth import AuthManager
from models.enums import RoleType
from bson.errors import InvalidId

class User:
    def __init__(self, db):
        self.users_collection = db["users"]

    def check_and_create_user_data(self, request):
        email = request.json.get('email')
        password = request.json.get('password')
        repeat_password = request.json.get('password2')

        if not email or not password:
            return {'message': 'Missing email or password'}, 400

        if password != repeat_password:
            return {'message': 'Wrong password'}, 400

        existing_user = self.users_collection.find_one({'email': email})
        if existing_user:
            return {'message': 'User already exists'}, 409

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        payload_dict = {
            'email': email,
            'password': hashed_password,
            'createdAt': datetime.now(),
            'isDeleted': False,
            'role': RoleType.new_user.value
        }
        return payload_dict

    def authenticate_user(self, request):
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return {'message': 'Missing email or password'}, 400

        login_user = self.users_collection.find_one({'email': email})
        if login_user and check_password_hash(login_user['password'], password):
            user_id = str(login_user['_id'])
            user_role = login_user.get('role', 'user')
            token = AuthManager.encode_token(user_id, user_role)
            return {"access_token": token, "user_id": user_id, "role": user_role}, 200

        return {'message': 'Wrong password or user not found'}, 401


    def update_user_role(self, user_id, new_role):
        if new_role not in [role.value for role in RoleType]:
            return {'error': 'Invalid role specified'}, 400


        try:
            oid = ObjectId(user_id)
        except InvalidId:
            print(f"Invalid user ID format: {user_id}")
            return {'error': 'Invalid user ID format'}, 400

        result = self.users_collection.update_one(
            {"_id": oid},
            {"$set": {"role": new_role}}
        )

        if result.modified_count == 0:
            return {'error': 'User not found or no update needed'}, 404

        return {'message': 'User role updated successfully'}, 200
