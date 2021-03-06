# coding:utf8
import logging
import json
from flask import current_app
import MySQLdb as mysql_db
from subprocess import Popen, PIPE
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import JSONWebSignatureSerializer as Serializer
from itsdangerous import TimedJSONWebSignatureSerializer as TSerializer
from . import db
import platform

if 'Linux' in platform.platform():
    logging.basicConfig(filename='/tmp/sqlguard.log', level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.DEBUG)


class Permission:
    APPLY = 1
    OPTIMIZE = 2
    EXECUTE = 4
    ADMIN = 1024


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    name_zh = db.Column(db.String(64), unique=True)
    desc = db.Column(db.String(128), nullable=True)
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': {
                'desc': '研发人员',
                'name_zh': '研发',
                'permissons': [Permission.APPLY, Permission.OPTIMIZE]
            },
            'Manager': {
                'desc': '经理（主管）',
                'name_zh': '经理',
                'permissons': [Permission.APPLY, Permission.OPTIMIZE, Permission.EXECUTE]
            },
            'Administrator': {
                'desc': '管理员',
                'name_zh': '管理员',
                'permissons': [Permission.APPLY, Permission.OPTIMIZE, Permission.EXECUTE, Permission.ADMIN]
            }
        }

        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(
                    name=r, name_zh=roles[r]['name_zh'], desc=roles[r]['desc'])
            role.reset_permission()
            for perm in roles[r]['permissons']:
                role.add_permission(perm)
            role.default = (default_role == role.name)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def to_json(self):
        json_role = {
            'id': self.id,
            'name': self.name,
            'name_zh': self.name_zh,
            'desc': self.desc
        }
        return json_role

    def __repr__(self):
        return '<Role %r>' % self.name


class Env(db.Model):
    __tablename__ = 'envs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    name_zh = db.Column(db.String(64), unique=True)
    desc = db.Column(db.String(128), nullable=True)
    default = db.Column(db.Boolean, default=False)
    mysqls = db.relationship('Mysql', backref='env', lazy='dynamic')

    @staticmethod
    def insert_envs():
        envs = {
            'Development': ['开发环境', 'Development'],
            'Staging': ['预发环境', 'Staging'],
            'Production': ['生产环境', 'Production']
        }

        default_env = 'Development'
        for e in envs:
            env = Env.query.filter_by(name=e).first()
            if env is None:
                env = Env(name=e, name_zh=envs[e][0], desc=envs[e][1])
            env.default = (default_env == env.name)
            db.session.add(env)
        db.session.commit()

    def to_json(self):
        json_env = {
            'id': self.id,
            'name': self.name,
            'name_zh': self.name_zh,
            'desc': self.desc
        }
        return json_env

    def __repr__(self):
        return '<Env %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    sqls = db.relationship('Sql', backref='user', lazy='dynamic')

    def __init__(self, **kargs):
        super(User, self).__init__(**kargs)
        if self.email == current_app.config['SQL_GUARD_ADMIN']:
            self.role_id = Role.query.filter_by(
                name='Administrator').first().id
        else:
            self.role_id = Role.query.filter_by(default=True).first().id

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_password_reset_token(self):
        s = TSerializer(
            current_app.config['SECRET_KEY'], current_app.config['PASSWORD_RESET_TOKEN_EXPIRATION_SECOND'])
        token = s.dumps({'id': self.id})
        return token.decode("utf-8")

    def reset_password(self, token, password):
        s = TSerializer(
            current_app.config['SECRET_KEY'], current_app.config['PASSWORD_RESET_TOKEN_EXPIRATION_SECOND'])
        try:
            data = s.loads(token)
        except:
            return False
        id = data.get('id')
        if id is None:
            return False
        if self.id == id:
            self.password = password
            db.session.commit()
            return True
        else:
            return False

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
            'name': self.name
        }
        return json_user

    def __repr__(self):
        return '<User %r>' % self.name


class Mysql(db.Model):
    __tablename__ = 'mysqls'
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(64), nullable=False)
    port = db.Column(db.String(10), default='3306')
    database = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(128), default='root')
    password_secret = db.Column(db.String(128), nullable=False)
    env_id = db.Column(db.Integer, db.ForeignKey('envs.id'))
    note = db.Column(db.String(128), nullable=True)
    sqls = db.relationship('Sql', backref='mysql', lazy="dynamic")

    def __init__(self, **kargs):
        super(Mysql, self).__init__(**kargs)
        env_id = kargs.get('env_id')
        if env_id is None:
            self.env_id = Env.query.filter_by(default=True).first().id

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        s = Serializer(current_app.config['SECRET_KEY'])
        self.password_secret = s.dumps({'password': password})

    def connect(self):
        pass

    def get_sqladvisor_check_result(self, sql):
        s = Serializer(current_app.config['SECRET_KEY'])
        password = s.loads(self.password_secret).get('password', '')
        cmd_prefix = "/usr/local/bin/sqladvisor -h {}  -P {}  -u {} -p '{}' -d {} -v 2 -q \"".format(
            self.host, self.port, self.username, password, self.database)
        sql = sql.replace('"', '\\"')
        sql = sql.replace('`', '\\`')
        cmd = cmd_prefix + sql + '"'

        print(cmd)
        logging.info(cmd)
        result_detail = Popen(
            cmd, stderr=PIPE, shell=True).stderr.read().strip('\n').strip()
        logging.info(result_detail)

        ok = True
        if 'SQLAdvisor结束' in result_detail:
            res_len = len(result_detail.split('错误日志'))
            if res_len > 1:
                result_detail = result_detail.split(
                    '错误日志')[1:res_len].strip(':')
                ok = False
        else:
            ok = False

        if ok:
            result = [line for line in result_detail.split(
                '\n') if line != ''][-2]
            result = result.split('：')[-1]
            if '[Note]' in result and 'SQL解析优化' in result:
                ok = False
                result = ''
        else:
            result = result_detail

        return result, result_detail, ok

    def get_inception_check_result(self, sql):
        return self.execute_in_inception(sql, check=True)

    def get_inception_execute_result(self, sql):
        return self.execute_in_inception(sql, check=False)

    def execute_in_inception(self, sql, check=True):
        inception_host = current_app.config['INCEPTION_HOST']
        inception_port = current_app.config['INCEPTION_PORT']

        s = Serializer(current_app.config['SECRET_KEY'])
        password = s.loads(self.password_secret).get('password', '')

        inception_extra_args = '/*--check=1;' if check else '/*--execute=1;'
        inception_extra_args += '--disable-remote-backup;'
        inception_prefix = '--user={};--password={};--host={};--port={};*/inception_magic_start;use {};'.format(
            self.username, password, self.host, self.port, self.database)

        if not sql.endswith(';'):
            sql = sql + ';'

        inception_suffix = 'inception_magic_commit;'
        full_inception_sql = inception_extra_args + \
            inception_prefix + sql + inception_suffix
        result_raw, ok = self.execute_inception_sql(
            inception_host, inception_port, full_inception_sql)

        if ok:
            result_detail = []
            result = []
            for row in result_raw:
                logging.debug(row)
                # http://mysql-inception.github.io/inception-document/results/#inception
                if check:
                    result_detail.append(row[5] + "|" + row[4])
                    if row[4] != 'None':
                        result.append(row[5] + "|" + row[4])
                else:
                    result_detail.append(row[5] + "|" + row[4] + "|" + str(row[6]))
                    result.append(row[5] + "|" + row[4] + "|" + str(row[6]))
            return "||".join(result), json.dumps(result_detail), ok

        return result_raw, result_raw, ok

    def execute_inception_sql(self, host, port, sql):
        try:
            conn = mysql_db.connect(host=host, user='',
                                    passwd='', db='', port=int(port))
            cur = conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            # num_fields = len(cur.description)
            # field_names = [i[0] for i in cur.description]
            cur.close()
            conn.close()
            return result, True
        except Exception as e:
            errMsg = "Mysql Error {}: {}".format(e.args[0], e.args[1])
            return errMsg, False

    def to_json(self):
        json_mysql = {
            'id': self.id,
            'host': self.host,
            'port': self.port,
            'database': self.database
        }
        return json_mysql

    def __repr__(self):
        return '<Mysql %r %r %r>' % (self.host, self.port, self.database)


SqlType = {
    'SQLADVISOR': 0,
    'INCEPTION': 1
}


SqlStatus = {
    'AUDIT': 0,
    'CHEKING': 1,
    'EXECUTING': 2,
    'DONE': 3,
    'FAILURE': -1,
}


class Sql(db.Model):
    __tablename__ = 'sqls'
    id = db.Column(db.Integer, primary_key=True)
    sql = db.Column(db.Text)
    type = db.Column(db.Integer, default=SqlType['SQLADVISOR'])
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    mysql_id = db.Column(db.Integer, db.ForeignKey('mysqls.id'))
    reviewer_id = db.Column(db.Integer, default=0)
    note = db.Column(db.String(128), nullable=True)
    result = db.Column(db.Text)
    result_detail = db.Column(db.Text)
    result_execute = db.Column(db.Text)
    result_detail_execute = db.Column(db.Text)

    def __init__(self, **kargs):
        super(Sql, self).__init__(**kargs)
        type = kargs.get('type', SqlType['SQLADVISOR'])
        if type not in SqlType.values():
            self.type = SqlType['SQLADVISOR']
        if self.type == SqlType['INCEPTION']:
            self.status = SqlStatus['AUDIT']
        else:
            self.status = SqlStatus['CHEKING']

    @staticmethod
    def on_changed_sql(target, value, oldvalue, initiator):
        print('--------------->', target, initiator)
        mysql = Sql.query.get(target.id).mysql
        target.result = mysql.get_sqladvisor_result(value)

    def get_sqladvisor_result(self):
        return self.mysql.get_sqladvisor_check_result(self.sql)

    def check(self):
        if self.type == SqlType['SQLADVISOR']:
            return self.mysql.get_sqladvisor_check_result(self.sql)
        elif self.type == SqlType['INCEPTION']:
            return self.mysql.get_inception_check_result(self.sql)
        else:
            return '', '', False

    def execute(self):
        if self.type == SqlType['INCEPTION']:
            return self.mysql.get_inception_execute_result(self.sql)
        else:
            return '', '', False

    def to_json(self):
        json_sql = {
            'id': self.id,
            'sql': self.sql,
            'type': self.type,
            'status': self.status,
            'result': self.result
        }
        return json_sql

    def __repr__(self):
        return '<Sql %r>' % self.sql


# db.event.listen(Sql.sql, 'set', Sql.on_changed_sql)
