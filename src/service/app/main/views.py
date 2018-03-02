from flask import request, jsonify
import logging
from app import db
from . import main
from ..models import Sql, Mysql
from ..schemas import MysqlSchema, MysqlPostSchema, SqlSchema, SqlPostSchema
from ..errors import bad_request, unauthorized, forbidden, conflict

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


@main.route('/mysqls', methods=['POST'])
def create_mysql():
    data = request.json
    mysql_post = MysqlPostSchema().get_mysql_or_error(data)
    port = mysql_post.port if mysql_post.port else 3306
    mysql = Mysql.query.filter_by(
        host=mysql_post.host, port=port,
        database=mysql_post.database,
        env_id=mysql_post.env_id).first()
    if mysql:
        return conflict('数据库已存在')
    db.session.add(mysql_post)
    db.session.commit()
    return jsonify(MysqlSchema().dump(mysql_post).data), 201


@main.route('/mysql/<int:id>')
def get_mysql(id):
    mysql = Mysql.get_or_404(id)
    return jsonify(MysqlSchema().dump(mysql).data)


@main.route('/mysql/<int:id>', methods=['PUT'])
def edit_mysql():
    pass


@main.route('/sqls', methods=['POST'])
def create_sql():
    data = request.json
    sql_post = SqlPostSchema().get_sql_or_error(data)
    db.session.add(sql_post)
    db.session.commit()
    return jsonify(SqlSchema().dump(sql_post).data), 201


@main.route('/sql/<int:id>')
def get_sql():
    sql = Sql.get_or_404(id)
    return jsonify(SqlSchema().dump(sql).data)


@main.route('/sql/<int:id>', methods=['PUT'])
def edit_sql():
    pass
