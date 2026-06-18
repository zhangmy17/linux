from flask import Flask, request, jsonify
from functools import wraps
import jwt
import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-12345'

USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split(' ')[1] if ' ' in token else token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/api/token', methods=['POST'])
def get_token():
    """工具2：获取鉴权token（不需要鉴权）"""
    auth_data = request.get_json()
    username = auth_data.get('username') if auth_data else None
    password = auth_data.get('password') if auth_data else None

    if not username or not password:
        return jsonify({'message': '请提供用户名和密码'}), 400

    user = USERS.get(username)
    if not user or user['password'] != password:
        return jsonify({'message': '用户名或密码错误'}), 401

    token = jwt.encode({
        'username': username,
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        'token': token,
        'username': username,
        'role': user['role'],
        'expires_in': '24 hours'
    })


@app.route('/api/user/info', methods=['GET'])
@token_required
def get_user_info(current_user):
    """工具1：获取用户信息（需要鉴权）"""
    user = USERS.get(current_user)
    return jsonify({
        'username': current_user,
        'role': user['role'] if user else 'unknown',
        'login_time': datetime.datetime.now().isoformat()
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'mcp-auth-service'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)