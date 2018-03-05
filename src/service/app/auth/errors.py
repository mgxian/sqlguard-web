import json
from . import auth
from flask import jsonify
from ..execeptions import ValidationError


@auth.errorhandler(ValidationError)
def myerror(e):
    try:
        msg = json.loads(str(e))
        response = jsonify({'msg': msg})
    except:
        response = jsonify({'msg': str(e)})
    response.status_code = 400
    return response
