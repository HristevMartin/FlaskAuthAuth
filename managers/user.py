from datetime import datetime

from bson import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash

from managers.auth import AuthManager
from models.enums import RoleType


class User:
    def __init__(self, db):
        self.users_collection = db["users"]

    def check_and_create_user_data(self, request):
        email = request.json.get("email")
        password = request.json.get("password")
        repeat_password = request.json.get("password2")
        role = request.json.get("role")

        if not email or not password:
            return {"message": "Missing email or password"}, 400

        if password != repeat_password:
            return {"message": "Wrong password"}, 400

        existing_user = self.users_collection.find_one({"email": email})
        if existing_user:
            return {"message": "User already exists"}, 409

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        payload_dict = {
            "email": email,
            "password": hashed_password,
            "createdAt": datetime.now(),
            "isDeleted": False,
            "role": [role] if role else [RoleType.NEW_USER.value],
        }
        return payload_dict

    def authenticate_user(self, request):
        email = request.json.get("email")
        password = request.json.get("password")

        if not email or not password:
            return {"message": "Missing email or password"}, 400

        login_user = self.users_collection.find_one({"email": email})
        if login_user and check_password_hash(login_user["password"], password):
            user_id = str(login_user["_id"])
            user_role = login_user.get("role", "user")
            token = AuthManager.encode_token(user_id, user_role)
            return {"access_token": token, "user_id": user_id, "role": user_role}, 200

        return {"message": "Wrong password or user not found"}, 401

    def add_role_to_user(self, user_id, new_role):
        if new_role not in [role.value for role in RoleType]:
            return {"message": "Invalid role"}, 400

        result = self.users_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$addToSet": {"role": new_role}}
        )
        if result.modified_count == 0:
            return {"message": "Role already exists or user not found"}, 409
        return {"message": "Role added successfully"}, 200

    def remove_role_from_user(self, user_id, role):
        if role not in [role.value for role in RoleType]:
            return {"message": "Invalid role"}, 400

        result = self.users_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$pull": {"role": role}}
        )

        print("MongoDB operation result:", result.raw_result)

        if result.modified_count == 0:
            return {"message": "Role not found or user not found"}, 404
        return {"message": "Role removed successfully"}, 200
