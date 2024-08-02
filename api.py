from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mongo
from managers.auth import AuthManager, auth
from models.enums import RoleType
from util.decorators import permission_required

api = Blueprint('api', __name__)

@api.route('/some')
@auth.login_required
@permission_required(RoleType.new_user)
def protected():
    return jsonify({"msg": "Welcome Admin!"}), 200


@api.route('/register', methods=['POST'])
def register():
    users = mongo.db.users
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400
    existing_user = users.find_one({'email': email})
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    users.insert_one({
        'email': email,
        'password': hashed_password,
        'createdAt': datetime.now(),
        'isDeleted': False,
        'role': 'user'
    })
    return jsonify({'message': 'User created successfully', 'role': 'user'}), 201


@api.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'email': request.json['email']})
    if login_user and check_password_hash(login_user['password'], request.json['password']):
        user_id = str(login_user['_id'])
        user_role = login_user.get('role', 'user')
        token = AuthManager.encode_token(user_id, user_role)
        return jsonify({"access_token": token, "user_id": user_id, "role": user_role}), 200
    return jsonify({'message': 'Wrong password or user not found'}), 401

@api.route('/')
def hello_world():
    return 'Hello World!'
