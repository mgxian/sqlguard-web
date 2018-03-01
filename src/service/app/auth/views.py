from . import auth
from ..models import User
from ..schemas import UserSchema, UserPostSchema
import json
from flask import request, jsonify


@auth.route('/users', methods=['POST'])
def create_user():
    data = request.json
    validate_result = UserPostSchema().load(data)
    print(validate_result)
    return jsonify(data)
