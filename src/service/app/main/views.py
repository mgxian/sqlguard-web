# coding:utf8
from flask import request, jsonify, g, abort
import logging
import json
from app import db
from . import main
from ..models import Sql, Mysql, Env, SqlType, SqlStatus, Permission, Role, User
from ..schemas import MysqlSchema, MysqlPutSchema, MysqlPostSchema, SqlSchema, SqlPutSchema, SqlPostSchema, EnvSchema, RoleSchema
from ..errors import bad_request, unauthorized, forbidden, conflict
from flask_jwt import jwt_required, current_identity
from ..decorators import permission_required
from flask import current_app
import jwt

logging.basicConfig(level=logging.DEBUG)


@main.route('/envs')
@jwt_required()
def get_envs():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    envs = Env.query.paginate(page=page, per_page=per_page).items
    envs_json = EnvSchema(many=True).dump(envs).data
    return jsonify(envs_json)


@main.route('/roles')
@jwt_required()
def get_roles():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    roles = Role.query.paginate(page=page, per_page=per_page).items
    roles_json = RoleSchema(many=True).dump(roles).data
    return jsonify(roles_json)


@main.route('/mysqls')
@jwt_required()
def get_mysqls():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    env_id = request.args.get('env_id')
    if env_id is None:
        mysqls = Mysql.query.paginate(page=page, per_page=per_page).items
    else:
        mysqls = Env.query.get(env_id).mysqls

    mysqls_json = MysqlSchema(many=True).dump(mysqls).data
    for idx, mysql in enumerate(mysqls):
        mysqls_json[idx]['env'] = {
            'id': mysql.env.id,
            'name': mysql.env.name,
            'name_zh': mysql.env.name_zh
        }
    return jsonify(mysqls_json)


@main.route('/mysqls', methods=['POST'])
@jwt_required()
@permission_required(Permission.EXECUTE)
def create_mysql():
    data = request.json
    mysql_post = MysqlPostSchema().get_mysql_or_error(data)
    port = mysql_post.port if mysql_post.port else 3306
    if mysql_post.env_id:
        env_id = mysql_post.env_id
    else:
        env_id = Env.query.filter_by(default=True).first().id
    mysql = Mysql.query.filter_by(
        host=mysql_post.host, port=port,
        database=mysql_post.database,
        env_id=env_id).first()
    if mysql:
        return conflict('数据库已存在')
    db.session.add(mysql_post)
    db.session.commit()
    mysql_json = MysqlSchema().dump(mysql_post).data
    mysql_json['env'] = {
        'id': mysql_post.env.id,
        'name': mysql_post.env.name,
        'name_zh': mysql_post.env.name_zh
    }
    return jsonify(mysql_json), 201


@main.route('/mysql/<int:id>')
@jwt_required()
def get_mysql(id):
    mysql = Mysql.query.get_or_404(id)
    mysql_json = MysqlSchema().dump(mysql).data
    mysql_json['env'] = {
        'id': mysql.env.id,
        'name': mysql.env.name,
        'name_zh': mysql.env.name_zh
    }
    return jsonify(mysql_json)


@main.route('/mysql/<int:id>', methods=['PUT'])
@jwt_required()
@permission_required(Permission.EXECUTE)
def edit_mysql(id):
    mysql = Mysql.query.get_or_404(id)
    data = request.json
    mysql_put = MysqlPutSchema().get_mysql_or_error(data)
    port = mysql_put.port if mysql_put.port else 3306
    if mysql_put.env_id:
        env_id = mysql_put.env_id
    else:
        # env_id = Env.query.filter_by(default=True).first().id
        env_id = mysql.env_id
    mysql_check = Mysql.query.filter_by(
        host=mysql_put.host, port=port,
        database=mysql_put.database,
        env_id=env_id).first()
    print(env_id)
    if mysql_check and mysql_check.id != id:
        return conflict('数据库已存在')
    env_id = data.get('env_id')
    password = data.get('password')
    if env_id is None:
        mysql_put.env_id = mysql.env_id
    if mysql_put.host:
        mysql.host = mysql_put.host
    if mysql_put.port:
        mysql.port = mysql_put.port
    if mysql_put.database:
        mysql.database = mysql_put.database
    if mysql_put.username:
        mysql.username = mysql_put.username
    if mysql_put.env_id:
        mysql.env_id = mysql_put.env_id
    if password and password.strip() != "":
        mysql.password = password.strip()
    mysql.note = mysql_put.note
    db.session.commit()
    mysql_json = MysqlSchema().dump(mysql).data
    mysql_json['env'] = {
        'id': mysql.env.id,
        'name': mysql.env.name,
        'name_zh': mysql.env.name_zh
    }
    return jsonify(mysql_json)


@main.route('/mysql/<int:id>', methods=['DELETE'])
@jwt_required()
@permission_required(Permission.EXECUTE)
def delete_mysql(id):
    mysql = Mysql.query.get_or_404(id)
    db.session.delete(mysql)
    db.session.commit()
    return ('', 200)


@main.route('/mysql/<int:mysql_id>/sqls')
@jwt_required()
def get_sqls(mysql_id):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    mysql = Mysql.query.get_or_404(mysql_id)
    sqls = mysql.sqls.paginate(page=page, per_page=per_page).items
    sqls_json = SqlSchema(many=True).dump(sqls).data
    return jsonify(sqls_json)


@main.route('/mysql/<int:mysql_id>/sqls', methods=['POST'])
@jwt_required()
def create_sql(mysql_id):
    data = request.json
    sql_post = SqlPostSchema().get_sql_or_error(data)
    sql_post.user_id = current_identity.id
    sql_post.mysql_id = mysql_id
    mysql = Mysql.query.get_or_404(mysql_id)

    if sql_post.type == SqlType['SQLADVISOR']:
        sql_post.result_detail = mysql.get_sqladvisor_check_result(
            sql_post.sql)
        result = [line for line in sql_post.result_detail.split(
            '\n') if line != ''][-2]
        sql_post.result = result.split('：')[-1]
        logging.debug(sql_post.result)
    elif sql_post.type == SqlType['INCEPTION']:
        result_detail = mysql.get_inception_check_result(sql_post.sql)
        sql_post.result_detail = result_detail
        result = []
        for row in json.loads(result_detail):
            msg = row.split('|')[1]
            if msg != 'None':
                result.append(row)
        logging.debug(result)
        sql_post.result = '||'.join(result)
        if len(result) != 0:
            return jsonify(SqlSchema().dump(sql_post).data), 400
    else:
        sql_post.result = 'not support type'

    db.session.add(sql_post)
    db.session.commit()
    return jsonify(SqlSchema().dump(sql_post).data), 201


@main.route('/mysql/<int:mysql_id>/sql/<int:id>')
@jwt_required()
def get_sql(mysql_id, id):
    sql = Sql.query.filter_by(mysql_id=mysql_id, id=id).first()
    if sql:
        return jsonify(SqlSchema().dump(sql).data)
    else:
        return abort(404)


@main.route('/mysql/<int:mysql_id>/sql/<int:id>', methods=['PUT'])
@jwt_required()
def edit_sql(mysql_id, id):
    sql = Sql.query.filter_by(mysql_id=mysql_id, id=id).first()
    if sql is None:
        return abort(404)
    data = request.json
    sql_put = SqlPutSchema().get_sql_or_error(data)
    if sql_put.sql:
        sql.sql = sql_put.sql
        sql.result = ''
    db.session.commit()
    return jsonify(SqlSchema().dump(sql).data)


@main.route('/mysql/<int:mysql_id>/sql/<int:id>/check', methods=['POST'])
@jwt_required()
def check_sql(mysql_id, id):
    sql = Sql.query.filter_by(mysql_id=mysql_id, id=id).first()
    if sql is None:
        return abort(404)
    sql.result = sql.check()
    print(sql.result)
    db.session.commit()
    return ('', 200)


@main.route('/mysql/<int:mysql_id>/sql/<int:id>/execute', methods=['POST'])
@jwt_required()
@permission_required(Permission.EXECUTE)
def execute_sql(mysql_id, id):
    sql = Sql.query.filter_by(mysql_id=mysql_id, id=id).first()
    if sql is None:
        return abort(404)
    sql.result = sql.execute()
    sql.status = SqlStatus['DONE']
    print(sql.result)
    db.session.commit()
    return ('', 200)


@main.route('/user/<int:id>/role', methods=['POST'])
@jwt_required()
@permission_required(Permission.ADMIN)
def assign_role(id):
    user = User.query.get_or_404(id)
    if not request.is_json:
        return bad_request('need payload')
    role_id = request.json.get('role_id')
    if role_id is None:
        return bad_request('nedd role_id')
    user.role_id = role_id
    db.session.commit()
    return ('', 200)


@main.route('/user/sqls')
@jwt_required()
def get_user_sqls():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    type = request.args.get('type', SqlType['SQLADVISOR'])
    user_id = current_identity.id
    sqls = Sql.query.filter_by(user_id=user_id).filter(
        Sql.type == type).paginate(page=page, per_page=per_page).items
    sqls_json = SqlSchema(many=True).dump(sqls).data
    for i, sql in enumerate(sqls):
        mysql_tmp = sql.mysql
        sqls_json[i]['mysql'] = {
            'id': mysql_tmp.id,
            'database': mysql_tmp.database,
            'env': {
                'name': mysql_tmp.env.name,
                'name_zh': mysql_tmp.env.name_zh
            }
        }
    return jsonify(sqls_json)


@main.route('/sqls')
@jwt_required()
@permission_required(Permission.EXECUTE)
def get_sqls_by_status():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    status = request.args.get('status')
    if status:
        sqls = Sql.query.filter_by(status=status, type=SqlType['INCEPTION']).paginate(
            page=page, per_page=per_page).items
    else:
        sqls = Sql.query.filter_by(type=SqlType['INCEPTION']).filter(Sql.status != status).paginate(
            page=page, per_page=per_page).items
    sqls_json = SqlSchema(many=True).dump(sqls).data
    return jsonify(sqls_json)
