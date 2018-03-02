from flask import jsonify


def conflict(msg):
    response = jsonify({'msg': msg})
    response.status_code = 409
    return response


def forbidden(msg):
    response = jsonify({'msg': msg})
    response.status_code = 403
    return response


def unauthorized(msg):
    response = jsonify({'msg': msg})
    response.status_code = 401
    return response


def bad_request(msg):
    response = jsonify({'msg': msg})
    response.status_code = 400
    return response
