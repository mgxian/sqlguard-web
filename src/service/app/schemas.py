from . import db
from . import ma
from .execeptions import ValidationError
from .models import User, Role, Env, Mysql, Sql
from marshmallow import fields, post_load
import json

# from marshmallow import fields, Schema, post_load, ValidationError
# name = fields.Str(required=True)
# email = fields.Email(required=True)

# @post_load
# def make_user(self, data):
#     print('d----', data)
#     return User(**data)
#    try:
#         role = Role.query.filter_by(name='User').first()
#         role_schema = RoleSchema()
#         data = role_schema.dump(role).data
#         print(jsonify(data))
#     except ValidationError as err:
#         print(err.messages)
#         print(err.valid_data)


class UserSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'name', 'username', 'email')
        model = User


class EnvSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'name', 'desc')
        model = Env


class RoleSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'name', 'desc')
        model = Role


class MysqlSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'host', 'port', 'database', 'username', 'env_id')
        model = Mysql


class SqlSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'sql', 'result', 'type', 'status')
        model = Sql


class UserPutSchema(ma.Schema):
    email = fields.Email()
    name = fields.Str()

    @post_load
    def make_user(self, data):
        u = User(**data)
        return u

    def get_user_or_error(self, data):
        result = self.load(data)
        d = result.data
        e = result.errors
        if e:
            raise ValidationError(json.dumps(e))
        else:
            return d


class UserPostSchema(UserPutSchema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)


class MysqlPutSchema(ma.Schema):
    host = fields.Str()
    port = fields.Int()
    database = fields.Str()
    username = fields.Str()
    env_id = fields.Int()

    @post_load
    def make_mysql(self, data):
        m = Mysql(**data)
        return m

    def get_mysql_or_error(self, data):
        result = self.load(data)
        d = result.data
        e = result.errors
        if e:
            raise ValidationError(json.dumps(e))
        else:
            env = Env.query.get(data.get('env_id'))
            if env is None:
                raise ValidationError(json.dumps({'env_id': 'env_id error'}))
            return d


class MysqlPostSchema(MysqlPutSchema):
    host = fields.Str(required=True)
    database = fields.Str(required=True)
    password = fields.Str(required=True)


class SqlPutSchema(ma.Schema):
    sql = fields.Str()
    type = fields.Int()

    @post_load
    def make_sql(self, data):
        s = Sql(**data)
        return s

    def get_sql_or_error(self, data):
        result = self.load(data)
        d = result.data
        e = result.errors
        if e:
            raise ValidationError(json.dumps(e))
        else:
            return d


class SqlPostSchema(SqlPutSchema):
    sql = fields.Str(required=True)


def test():
    role = Role.query.filter_by(name='User').first()
    role_schema = RoleSchema()
    data = role_schema.dump(role).data
    print(json.dumps(data))
