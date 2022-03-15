"""add seats to course sections

Revision ID: 53f333149502
Revises: 4da0df6b49e7
Create Date: 2020-12-04 17:00:43.425130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53f333149502'
down_revision = '4da0df6b49e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('seats_filled', sa.INTEGER(), nullable=True))
    op.add_column('course', sa.Column('seats_open', sa.INTEGER(), nullable=True))
    op.add_column('course', sa.Column('seats_total', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('course', 'seats_total')
    op.drop_column('course', 'seats_open')
    op.drop_column('course', 'seats_filled')
    # ### end Alembic commands ###
