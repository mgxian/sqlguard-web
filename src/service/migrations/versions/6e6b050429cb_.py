"""empty message

Revision ID: 6e6b050429cb
Revises: eeca51fb470e
Create Date: 2018-03-02 16:39:54.322821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e6b050429cb'
down_revision = 'eeca51fb470e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sqls', sa.Column('status', sa.Integer(), nullable=True))
    op.add_column('sqls', sa.Column('type', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sqls', 'type')
    op.drop_column('sqls', 'status')
    # ### end Alembic commands ###
