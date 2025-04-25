from flask import Blueprint, request, jsonify

# 模拟用户数据存储，实际应用中应使用数据库
users = {}
# 创建蓝图
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "用户名和密码不能为空"}), 400
    if username in users:
        return jsonify({"message": "用户名已存在"}), 400

    users[username] = password
    return jsonify({"message": "注册成功"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "用户名和密码不能为空"}), 400

    stored_password = users.get(username)
    if stored_password is None or stored_password != password:
        return jsonify({"message": "用户名或密码错误"}), 401

    return jsonify({"message": "登录成功"}), 200
