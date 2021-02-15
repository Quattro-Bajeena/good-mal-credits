"""empty message

Revision ID: c6a9f7b2109c
Revises: 5ac2ec9ee1d3
Create Date: 2021-02-08 16:56:54.804024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6a9f7b2109c'
down_revision = '5ac2ec9ee1d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('page_status', sa.Column('scheduled_to_update', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('page_status', 'scheduled_to_update')
    # ### end Alembic commands ###