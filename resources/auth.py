from datetime import datetime, timedelta

from bson import ObjectId
from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from db_extensions import mongo
from managers.auth import auth
from managers.user import User
from models.enums import RoleType
from util.decorators import permission_required


class Register(Resource):
    # @validate_schema(ComplainerRegisterRequestSchema)
    def post(self):
        user_table = mongo.db.users
        user_manager = User(mongo.db)
        result = user_manager.check_and_create_user_data(request)

        if isinstance(result, dict):
            user_table.insert_one(result)
            return {'message': 'User created successfully', 'role': 'user'}, 201
        else:
            return result


class Login(Resource):
    # @validate_schema(ComplainerLoginRequestSchema)
    def post(self):
        user_manager = User(mongo.db)
        result, status = user_manager.authenticate_user(request)
        return result, status


class UpdateUserRole(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    def patch(self, user_id):
        new_role = request.json.get('new_role')
        action = request.json.get('action')

        if not new_role:
            return {'error': 'Missing role'}, 400

        user_manager = User(mongo.db)

        if action == 'add':
            return user_manager.add_role_to_user(user_id, new_role)
        elif action == 'remove':
            return user_manager.remove_role_from_user(user_id, new_role)
        else:
            return {'error': 'Invalid action specified'}, 400


class InsertAdminUser(Resource):
    def get(self):
        user_table = mongo.db.users

        admin_user = {
            '_id': ObjectId(),
            'email': 'admin@gmail.com',
            'password': generate_password_hash('root', method='pbkdf2:sha256'),
            'createdAt': datetime.utcnow(),
            'isDeleted': False,
            'role': RoleType.admin.value
        }

        user_table.insert_one(admin_user)
        return {'message': 'Admin user created successfully'}, 201


class Logout(Resource):
    @auth.login_required
    def delete(self):
        current_user = auth.current_user()

        if not current_user:
            return {'message': 'Invalid user session'}, 401

        token = request.headers.get('Authorization').split(" ")[1]
        expires_at = datetime.utcnow() + timedelta(days=1)

        try:
            mongo.db.blacklisted_tokens.insert_one({
                "token": token,
                "expiresAt": expires_at,
                "blacklistedAt": datetime.utcnow(),
                "reason": "User logged out",
                "userId": current_user['_id'],
                "email": current_user['email'],
                "role": current_user['role']
            })

            return {'message': 'Logged out successfully'}, 200
        except Exception as e:
            print('Failed to blacklist token:', str(e))
            return {'message': 'Failed to logout'}, 500


class Test(Resource):
    @auth.login_required
    @permission_required(RoleType.new_user, RoleType.admin)
    def get(self):
        return {"message": "Hello World!"}
