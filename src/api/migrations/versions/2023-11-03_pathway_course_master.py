"""CoursesMaster table

Revision ID: ffaaeebb8125
Revises: efef12345678
Create Date: 2023-04-06 00:55:10.389370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffaaeebb8125'  # randomly created an 'unique id' with 12 hex characters
down_revision = 'efef12345678'  # grab value from previous version file
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('course_master',
    sa.Column('min_credits', sa.INTEGER, nullable=False),
    sa.Column('max_credits', sa.INTEGER, nullable=False),
    sa.Column('department', sa.VARCHAR(length=255), nullable=False),
    sa.Column('level', sa.INTEGER, nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), nullable=False),
    sa.Column('full_title', sa.TEXT, nullable=True),
    sa.Column('raw_precoreqs', sa.TEXT, nullable=True),
    sa.Column('school', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('min_credits', 'max_credits', 'department', 'level', 'title'),
    )
