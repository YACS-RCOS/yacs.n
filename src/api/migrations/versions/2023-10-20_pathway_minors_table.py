"""Minors table

Revision ID: efef12345678
Revises: abcd12345678
Create Date: 2023-04-06 00:55:10.389370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efef12345678'  # randomly created an 'unique id' with 12 hex characters
down_revision = 'fedcba100000'  # grab value from previous version file
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pathway_minors',
    sa.Column('minor', sa.VARCHAR(length=255), nullable=False),
    sa.Column('pathway', sa.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('minor', 'pathway'),
    )
