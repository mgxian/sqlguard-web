import json
from . import main
from flask import jsonify
from ..execeptions import ValidationError


@main.errorhandler(ValidationError)
def myerror(e):
    try:
        msg = json.loads(str(e))
        response = jsonify({'msg': msg})
    except:
        response = jsonify({'msg': str(e)})
    response.status_code = 400
    return response
