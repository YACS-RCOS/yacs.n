"""Professor_table

Revision ID: 95cb2a021aa9
Revises: 54df4fb8dfe9
Create Date: 2023-04-06 00:55:10.389370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95cb2a021aa9'
down_revision = '54df4fb8dfe9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #CHANGE COLUMNS
    op.create_table('professor',
    sa.Column('email', sa.VARCHAR(length=255), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('phone_number', sa.VARCHAR(length=255), nullable=True),
    sa.Column('department', sa.VARCHAR(length=255), nullable=True),
    sa.Column('office_room', sa.VARCHAR(length=255), nullable=True),
    sa.Column('classes', sa.VARCHAR(length=255), nullable=True),
    sa.Column('office_hours_time', sa.VARCHAR(length=255), nullable=True),
    sa.Column('rcs', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('email')
    )
    # ### end Alembic commands ###


# def downgrade():
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.drop_table('professor')
    # ### end Alembic commands ###
