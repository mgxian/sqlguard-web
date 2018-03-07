# coding:utf8
import json
from . import auth
from app import db
from ..models import User
from ..execeptions import ValidationError
from ..schemas import UserSchema, UserPutSchema, UserPostSchema
from ..errors import bad_request, unauthorized, forbidden, conflict
from flask import request, jsonify, abort, g


@auth.before_request
def before_request():
    g.user_id = 1


@auth.route('/users')
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
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(UserSchema().dump(user).data)


@auth.route('/user/<int:id>', methods=['PUT'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if user.id != g.user_id:
        return forbidden('你没有修改权限')
    data = request.json
    user_put = UserPutSchema().get_user_or_error(data)
    if user_put.name:
        user.name = user_put.name
    db.session.commit()
    return jsonify(UserSchema().dump(user).data)


@auth.route('/user/<int:id>/change_password', methods=['POST'])
def change_password(id):
    pass


@auth.route('/user/<int:id>/rest_password', methods=['POST'])
def rest_password(id):
    pass


@auth.route('/oauth2/token', methods=['POST'])
def create_token():
    pass
