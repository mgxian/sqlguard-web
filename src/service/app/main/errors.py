# coding:utf8
import json
from . import main
from flask import jsonify
from ..execeptions import ValidationError


@main.app_errorhandler(ValidationError)
def myerror(e):
    try:
        msg = json.loads(str(e))
        response = jsonify({'msg': msg})
    except:
        response = jsonify({'msg': str(e)})
    response.status_code = 400
    return response

@main.app_errorhandler(401)
def unauthorized(e):
    msg = "你没有足够的权限"
    response = jsonify({'msg': msg})
    response.status_code = 401
    return response

@main.app_errorhandler(404)
def not_found(e):
    return ('', 404)


@main.app_errorhandler(500)
def internal_server_error(e):
    return ('', 500)
