"""add session type and instructor

Revision ID: 54df4fb8dfe9
Revises: a3be4710680d
Create Date: 2021-09-25 03:08:18.501929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54df4fb8dfe9'
down_revision = 'a3be4710680d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course_session', sa.Column('instructor', sa.VARCHAR(length=255), nullable=True))
    op.add_column('course_session', sa.Column('session_type', sa.VARCHAR(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('course_session', 'session_type')
    op.drop_column('course_session', 'instructor')
    # ### end Alembic commands ###
