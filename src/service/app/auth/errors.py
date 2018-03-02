import json
from . import auth
from flask import jsonify
from ..execeptions import ValidationError


@auth.errorhandler(400)
def bad_request(e):
    response = jsonify({'msg': 'bad request'})
    response.status_code = 400
    return response


@auth.errorhandler(ValidationError)
def myerror(e):
    msg = json.loads(str(e))
    response = jsonify({'msg': msg})
    response.status_code = 400
    return response
