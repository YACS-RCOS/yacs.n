"""admin_settings semester add unique constraint

Revision ID: a3be4710680d
Revises: 53f333149502
Create Date: 2021-02-16 01:00:16.113602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3be4710680d'
down_revision = '53f333149502'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'admin_settings', ['semester'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'admin_settings', type_='unique')
    # ### end Alembic commands ###
