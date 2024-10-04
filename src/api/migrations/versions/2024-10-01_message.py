"""<message>

Revision ID: c61849c08ba7
Revises: c959c263997f
Create Date: 2024-10-01 21:39:04.527563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c61849c08ba7'
down_revision = 'c959c263997f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.TEXT(), nullable=True),
    sa.Column('email', sa.TEXT(), nullable=False),
    sa.Column('phone', sa.TEXT(), nullable=True),
    sa.Column('password', sa.TEXT(), nullable=False),
    sa.Column('major', sa.TEXT(), nullable=True),
    sa.Column('degree', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.alter_column('user_account', 'password',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_account', 'password',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_table('test')
    # ### end Alembic commands ###
