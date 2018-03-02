from . import auth
from ..models import User
from ..execeptions import ValidationError
from ..schemas import UserSchema, UserPostSchema
import json
from flask import request, jsonify, abort


@auth.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = UserPostSchema().get_user_or_error(data)
    return jsonify(user)
