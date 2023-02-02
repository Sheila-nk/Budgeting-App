"""empty message

Revision ID: 45cdeaab00f3
Revises: 
Create Date: 2023-02-02 07:45:27.246138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45cdeaab00f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=20), nullable=False),
    sa.Column('lastname', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('budget',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('deposit_category', sa.String(length=20), nullable=True),
    sa.Column('deposit_description', sa.String(length=20), nullable=True),
    sa.Column('deposit_amount', sa.Integer(), nullable=True),
    sa.Column('withdraw_category', sa.String(length=20), nullable=True),
    sa.Column('withdraw_description', sa.String(length=20), nullable=True),
    sa.Column('withdraw_amount', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('budget')
    op.drop_table('user')
    # ### end Alembic commands ###
