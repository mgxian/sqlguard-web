import json
from . import main
from flask import jsonify
from ..execeptions import ValidationError


@main.errorhandler(ValidationError)
def myerror(e):
    msg = json.loads(str(e))
    response = jsonify({'msg': msg})
    response.status_code = 400
    return response
