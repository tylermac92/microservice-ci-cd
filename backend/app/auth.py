from flask import Blueprint, request, jsonify
from .models import User, db
from flask_jwt_extended import create_access_token
import datetime

bp = Blueprint('auth', __name__)

@bp.route('/auth/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({'error': 'Missing JSON'}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'User exists'}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201

@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(hours=1))
        return jsonify({'access_token': token})
    return jsonify({'error': 'Invalid credentials'}), 401
