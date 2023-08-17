"""create schedules table

Revision ID: f3a78ea012da
Revises: 95cb2a021aa9
Create Date: 2023-08-17 16:33:18.765291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3a78ea012da'
down_revision = '95cb2a021aa9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'dp_schedules',
        sa.Column('schedule_id', sa.Integer, primary_key=True),
        sa.Column('selected_classes', sa.JSON),
        sa.Column('degree', sa.String)
    )


def downgrade():
    op.drop_table('dp_schedules')
