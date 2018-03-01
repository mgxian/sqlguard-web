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
        fields = ('id', 'host', 'port', 'database', 'username')
        model = Mysql


class SqlSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'sql', 'result')
        model = Sql


class UserPostSchema(ma.Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)
    name = fields.Str()

    @post_load
    def make_user(self, data):
        u = User(**data)
        return u

    def valid_data(self, data):
        result = self.load(data)
        d = result.data
        e = result.errors


class MysqlPostSchema(ma.Schema):
    host = fields.Str(required=True)
    port = fields.Int()
    database = fields.Str(required=True)
    user = fields.Str()
    password = fields.Str()

    @post_load
    def make_mysql(self, data):
        m = Mysql(**data)
        return m


class SqlSchema(ma.Schema):
    sql = fields.Str(required=True)

    @post_load
    def make_sql(self, data):
        s = Sql(**data)
        return s


def test():
    role = Role.query.filter_by(name='User').first()
    role_schema = RoleSchema()
    data = role_schema.dump(role).data
    print(json.dumps(data))
