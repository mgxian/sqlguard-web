import os

basedir = os.path.abspath(os.path.dirname(__name__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQL_GUARD_ADMIN = os.environ.get('SQL_GUARD_ADMIN')
    INCEPTION_HOST = os.environ.get('INCEPTION_HOST') or '127.0.0.1'
    INCEPTION_PORT = os.environ.get('INCEPTION_PORT') or 5506
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQL_GUARD_SLOW_DB_QUERY_TIME = 0.5
    SQLALCHEMY_POOL_RECYCLE = 100

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class DockerConfig(ProdConfig):
    @classmethod
    def init_app(cls, app):
        ProdConfig.init_app(app)


config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'docker': DockerConfig,
    'default': DevConfig
}
