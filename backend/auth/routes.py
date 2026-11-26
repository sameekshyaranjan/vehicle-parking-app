from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jwt, verify_jwt_in_request
)
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
import re
from ..models.user import User
from ..app import db
from .demo import DEMO_ACCOUNTS, demo_login_available, find_demo_account
from .services import AuthService
auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()


def login_response(user, admin_login=False):
    role = 'admin' if user.is_admin else 'user'
    claims = {'is_admin': user.is_admin, 'username': user.username}
    if admin_login:
        claims['role'] = role
    access_token = create_access_token(identity=str(user.id), additional_claims=claims)
    refresh_token = create_refresh_token(identity=str(user.id))
    if admin_login:
        current_app.logger.info(f"Admin login: {user.username} from {request.remote_addr}")
    elif current_app.redis:
        current_app.redis.setex(
            f'user_session:{user.id}',
            int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()),
            access_token,
        )
    return jsonify({
        'error': False,
        'message': 'Admin login successful' if admin_login else 'Login successful',
        'data': {
            'user': {
                'id': user.id,
                'username': user.username,
                'fullname': user.fullname,
                'email': user.email,
                'is_admin': user.is_admin,
                'role': role,
            },
            'tokens': {'access_token': access_token, 'refresh_token': refresh_token},
        },
    }), 200


@auth_bp.route('/demo', methods=['GET'])
def demo_status():
    return jsonify({'enabled': demo_login_available()})


@auth_bp.route('/demo/<role>', methods=['POST'])
def demo_login(role):
    if role not in DEMO_ACCOUNTS or not demo_login_available():
        return jsonify({'error': True, 'message': 'Demo login is unavailable.'}), 404
    user = find_demo_account(role)
    if user is None:
        return jsonify({'error': True, 'message': 'Demo account has not been set up.'}), 503
    return login_response(user, admin_login=user.is_admin)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        required_fields = ['username', 'password', 'fullname', 'email', 'address', 'pin_code']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'error': True,
                    'message': f'Missing required field: {field}'
                }), 400
        validation_result = auth_service.validate_registration_data(data)
        if not validation_result['valid']:
            return jsonify({
                'error': True,
                'message': validation_result['message']
            }), 400
        existing_user = User.query.filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()
        if existing_user:
            if existing_user.username == data['username']:
                return jsonify({
                    'error': True,
                    'message': 'Username already exists'
                }), 409
            else:
                return jsonify({
                    'error': True,
                    'message': 'Email already registered'
                }), 409
        new_user = User(
            username=data['username'].lower().strip(),
            password=generate_password_hash(data['password']),
            fullname=data['fullname'].strip(),
            email=data['email'].lower().strip(),
            address=data['address'].strip(),
            pin_code=data['pin_code'].strip(),
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(
            identity=new_user.id,
            additional_claims={
                'is_admin': new_user.is_admin,
                'username': new_user.username
            }
        )
        refresh_token = create_refresh_token(identity=new_user.id)
        return jsonify({
            'error': False,
            'message': 'User registered successfully',
            'data': {
                'user': {
                    'id': new_user.id,
                    'username': new_user.username,
                    'fullname': new_user.fullname,
                    'email': new_user.email,
                    'is_admin': new_user.is_admin
                },
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {str(e)}")
        return jsonify({
            'error': True,
            'message': 'Registration failed due to server error'
        }), 500
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data.get('username') or not data.get('password'):
            return jsonify({
                'error': True,
                'message': 'Username and password are required'
            }), 400
        username = data['username'].lower().strip()
        password = data['password']
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({
                'error': True,
                'message': 'Invalid username or password'
            }), 401
        return login_response(user)
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({
            'error': True,
            'message': 'Login failed due to server error'
        }), 500
@auth_bp.route('/admin-login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        if not data.get('username') or not data.get('password'):
            return jsonify({
                'error': True,
                'message': 'Admin credentials are required'
            }), 400
        username = data['username'].lower().strip()
        password = data['password']
        user = User.query.filter_by(username=username, is_admin=True).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({
                'error': True,
                'message': 'Invalid admin credentials'
            }), 401
        return login_response(user, admin_login=True)
    except Exception as e:
        current_app.logger.error(f"Admin login error: {str(e)}")
        return jsonify({
            'error': True,
            'message': 'Admin login failed'
        }), 500
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({
                'error': True,
                'message': 'User not found'
            }), 404
        new_access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'is_admin': user.is_admin,
                'username': user.username
            }
        )
        return jsonify({
            'error': False,
            'message': 'Token refreshed successfully',
            'data': {
                'access_token': new_access_token
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Token refresh error: {str(e)}")
        return jsonify({
            'error': True,
            'message': 'Token refresh failed'
        }), 500
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        current_user_id = get_jwt_identity()
        jti = get_jwt()['jti']
        if current_app.redis:
            current_app.redis.setex(
                f"blacklisted_token:{jti}",
                int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()),
                "blacklisted"
            )
            current_app.redis.delete(f"user_session:{current_user_id}")
        return jsonify({
            'error': False,
            'message': 'Logged out successfully'
        }), 200
    except Exception as e:
        current_app.logger.error(f"Logout error: {str(e)}")
        return jsonify({
            'error': True,
            'message': 'Logout failed'
        }), 500
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({
                'error': True,
                'message': 'User not found'
            }), 404
        return jsonify({
            'error': False,
            'message': 'User information retrieved',
            'data': {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'fullname': user.fullname,
                    'email': user.email,
                    'address': user.address,
                    'pin_code': user.pin_code,
                    'is_admin': user.is_admin,
                    'role': 'admin' if user.is_admin else 'user'
                }
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get current user error: {str(e)}")
        return jsonify({
            'error': True,
            'message': 'Failed to retrieve user information'
        }), 500
@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({
                'error': True,
                'message': 'User not found'
            }), 404
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        if not all([current_password, new_password, confirm_password]):
            return jsonify({
                'error': True,
                'message': 'All password fields are required'
            }), 400
        if not check_password_hash(user.password, current_password):
            return jsonify({
                'error': True,
                'message': 'Current password is incorrect'
            }), 400
        if new_password != confirm_password:
            return jsonify({
                'error': True,
                'message': 'New passwords do not match'
            }), 400
        if not auth_service.validate_password_strength(new_password):
            return jsonify({
                'error': True,
                'message': 'Password must be at least 6 characters long'
            }), 400
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({
            'error': False,
            'message': 'Password changed successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Change password error: {str(e)}")
        return jsonify({
            'error': True,
            'message': 'Failed to change password'
        }), 500
@auth_bp.route('/check-token', methods=['POST'])
def check_if_token_revoked():
    try:
        verify_jwt_in_request()
        jti = get_jwt()['jti']
        if current_app.redis:
            token_in_blacklist = current_app.redis.get(f"blacklisted_token:{jti}")
            return jsonify({'revoked': bool(token_in_blacklist)})
        return jsonify({'revoked': False})
    except Exception:
        return jsonify({'revoked': True})
