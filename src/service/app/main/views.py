from flask import request, jsonify
import logging
from . import main
from ..models import Sql, Mysql

logging.basicConfig(level=logging.DEBUG)


@main.route('/sql', methods=['POST'])
def sql():
    data = request.json
    res = data["sql"]
    # logging.warning(res)
    return res


@main.route('/inception', methods=['POST'])
def sql_inception():
    data = request.json
    res = data["sql"]
    # logging.warning(res)
    return res
