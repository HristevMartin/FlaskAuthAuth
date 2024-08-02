from datetime import datetime

from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from db_extensions import mongo
from managers.auth import AuthManager, auth
from models.enums import RoleType
from util.decorators import permission_required


class Register(Resource):
    # @validate_schema(ComplainerRegisterRequestSchema)
    def post(self):
        users = mongo.db.users
        email = request.json.get('email')
        password = request.json.get('password')
        if not email or not password:
            return jsonify({'message': 'Missing email or password'}), 400
        existing_user = users.find_one({'email': email})
        if existing_user:
            return {'message': 'User already exists'}, 409
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        users.insert_one({
            'email': email,
            'password': hashed_password,
            'createdAt': datetime.now(),
            'isDeleted': False,
            'role': 'user'
        })
        return {'message': 'User created successfully', 'role': 'user'}, 201


class Login(Resource):
    # @validate_schema(ComplainerLoginRequestSchema)
    def post(self):
        users = mongo.db.users
        login_user = users.find_one({'email': request.json['email']})
        if login_user and check_password_hash(login_user['password'], request.json['password']):
            user_id = str(login_user['_id'])
            user_role = login_user.get('role', 'user')
            token = AuthManager.encode_token(user_id, user_role)
            return {"access_token": token, "user_id": user_id, "role": user_role}, 200
        return {'message': 'Wrong password or user not found'}, 401


class Test(Resource):
    # @auth.login_required
    @permission_required(RoleType.new_user)
    def get(self):
        return {"message": "Hello World!"}
