from flask import current_app
import _mysql as mysql_db
from subprocess import Popen, PIPE
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import JSONWebSignatureSerializer as Serializer
from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    desc = db.Column(db.String(128), nullable=True)
    default = db.Column(db.Boolean, default=False)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': '开发人员',
            'Manager': '经理',
            'Administrator': '管理员'
        }

        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r, desc=roles[r])
            role.default = (default_role == role.name)
            db.session.add(role)
        db.session.commit()

    def to_json(self):
        json_role = {
            'id': self.id,
            'name': self.name,
            'desc': self.desc
        }
        return json_role

    def __repr__(self):
        return '<Role %r>' % self.name


class Env(db.Model):
    __tablename__ = 'envs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    desc = db.Column(db.String(128), nullable=True)
    default = db.Column(db.Boolean, default=False)
    mysqls = db.relationship('Mysql', backref='env', lazy='dynamic')

    @staticmethod
    def insert_envs():
        envs = {
            'Development': 'Development',
            'Staging': 'Staging',
            'Production': 'Production'
        }

        default_env = 'Development'
        for e in envs:
            env = Env.query.filter_by(name=e).first()
            if env is None:
                env = Env(name=e, desc=envs[e])
            env.default = (default_env == env.name)
            db.session.add(env)
        db.session.commit()

    def to_json(self):
        json_env = {
            'id': self.id,
            'name': self.name,
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
    password_secret = db.Column(db.String(128), nullable=True)
    env_id = db.Column(db.Integer, db.ForeignKey('envs.id'))
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
        # logging.warning(cmd)
        # res = Popen(cmd, stderr=PIPE, shell=True).stderr.read()
        return cmd

    def get_inception_check_result(self, sql):
        return self.execute_in_inception(sql, check=True)

    def get_inception_execute_result(self, sql):
        return self.execute_in_inception(sql, check=False)

    def execute_in_inception(self, sql, check=True):
        inception_host = current_app.config['INCEPTION_HOST']
        inception_port = current_app.config['INCEPTION_HOST']

        s = Serializer(current_app.config['SECRET_KEY'])
        password = s.loads(self.password_secret).get('password', '')

        inception_extra_args = '/*--check=1;' if check else '/*--execute=1;'
        inception_prefix = '--user={};--password={};--host={};--port={};*/inception_magic_start;use {};'.format(
            self.username, password, self.host, self.port, self.database)

        if not sql.endswith(';'):
            sql = sql + ';'

        inception_suffix = 'inception_magic_commit;'
        full_inception_sql = inception_extra_args + \
            inception_prefix + sql + inception_suffix
        return full_inception_sql
        try:
            conn = mysql_db.connect(host=inception_host, user='',
                                    passwd='', db='', port=int(inception_port))
            cur = conn.cursor()
            ret = cur.execute(full_inception_sql)
            result = cur.fetchall()
            num_fields = len(cur.description)
            field_names = [i[0] for i in cur.description]
            print(field_names)
            res = ""
            for row in result:
                res += row[5] + "|" + row[4] + "|" + row[8] + "\n"
            cur.close()
            conn.close()
            return full_inception_sql + "\n" + res
        except mysql_db.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            return "error"

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
    result = db.Column(db.Text)

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
        return self.mysql.get_sqladvisor_result(self.sql)

    def check(self):
        if self.type == SqlType['SQLADVISOR']:
            result = self.mysql.get_sqladvisor_check_result(self.sql)
        elif self.type == SqlType['INCEPTION']:
            result = self.mysql.get_inception_check_result(self.sql)
        else:
            result = ''
        print('--------------->check ', result)
        return result

    def execute(self):
        if self.type == SqlType['INCEPTION']:
            result = self.mysql.get_inception_execute_result(self.sql)
        else:
            result = ''
        print('--------------->check ', result)
        return result

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


db.event.listen(Sql.sql, 'set', Sql.on_changed_sql)
