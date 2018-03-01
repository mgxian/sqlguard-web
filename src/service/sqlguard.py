import os
import sys
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, Role, Env, Sql, Mysql

try:
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
except:
    pass

# print('-----before create app--------')
app = create_app(os.getenv('SQL_GUARD_CONFIG') or 'default')
migrate = Migrate(app, db)
# print(app.config)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Env=Env, Mysql=Mysql, Sql=Sql)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()

    # create or update env
    Env.insert_envs()


@app.cli.command()
def test():
    from app.schemas import test
    test()


@app.cli.command()
def run():
    app.run('0.0.0.0')
