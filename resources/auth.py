from datetime import datetime

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
        new_role = request.json.get('role')
        if not new_role:
            return {'error': 'Missing role'}, 400

        user_manager = User(mongo.db)
        return user_manager.update_user_role(user_id, new_role)


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


class Test(Resource):
    @auth.login_required
    @permission_required(RoleType.new_user)
    def get(self):
        return {"message": "Hello World!"}
