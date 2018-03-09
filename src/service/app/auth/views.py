# coding:utf8
import json
from . import auth
from app import db
from ..models import User
from ..execeptions import ValidationError
from ..schemas import UserSchema, UserPutSchema, UserPostSchema
from ..errors import bad_request, unauthorized, forbidden, conflict
from flask import request, jsonify, abort, g, url_for, current_app
from flask_jwt import current_identity, jwt_required
import logging
from ..email import send_email


@auth.route('/users')
@jwt_required()
def get_users():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    users = User.query.paginate(page=page, per_page=per_page).items
    users_json = UserSchema(many=True).dump(users).data
    return jsonify(users_json)


@auth.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_post = UserPostSchema().get_user_or_error(data)
    user = User.query.filter_by(username=user_post.username).first()
    if user:
        return conflict('用户名已存在')
    user = User.query.filter_by(email=user_post.email).first()
    if user:
        return conflict('邮箱已注册')
    db.session.add(user_post)
    db.session.commit()
    user_json = UserSchema().dump(user_post).data
    return jsonify(user_json), 201


@auth.route('/user/<int:id>')
@jwt_required()
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(UserSchema().dump(user).data)


@auth.route('/user/<int:id>', methods=['PUT'])
@jwt_required()
def edit_user(id):
    user = User.query.get_or_404(id)
    if user.id != current_identity.id:
        return forbidden('你没有修改权限')
    data = request.json
    user_put = UserPutSchema().get_user_or_error(data)
    if user_put.name:
        user.name = user_put.name
    db.session.commit()
    return jsonify(UserSchema().dump(user).data)


@auth.route('/user/<int:id>/change_password', methods=['POST'])
@jwt_required()
def change_password(id):
    user = User.query.get_or_404(id)
    if user.id != current_identity.id:
        return forbidden('你没有修改权限')
    data = request.json
    password_old = data.get('password_old')
    password_new = data.get('password_new')
    if password_old is None:
        return bad_request("旧密码不能为空")
    if password_new is None:
        return bad_request("新密码不能为空")

    if not user.verify_password(password_old):
        return bad_request("旧密码不正确")

    user.password = password_new
    db.session.commit()

    return ('', 200)


@auth.route('/user/<string:username>/reset_password')
def mail_reset_password_token(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return ('', 404)
    token = user.generate_password_reset_token()
    subject = "重置密码"
    content = request.host_url + \
        current_app.config['PASSWORD_RESET_URI'][1:] + \
        '?username={}&token={}'.format(username, token)
    logging.debug(content)
    send_email(user.email, subject, content)
    return ('', 200)


@auth.route('/user/<string:username>/reset_password', methods=['POST'])
def reset_password(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return ('', 404)
    data = request.json
    if data is None:
        return bad_request('need payload')
    token = data.get('token')
    password = data.get('password')
    if token is None or password is None:
        return bad_request('请求参数不正确')
    if user.reset_password(token, password):
        return ('', 200)
    return bad_request('验证不成功')
