"""Staff and people pageupdate tables

Revision ID: 4944ac794689
Revises: 551fd481bc6b
Create Date: 2021-02-02 16:50:01.169163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4944ac794689'
down_revision = '551fd481bc6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people_page_update',
    sa.Column('mal_id', sa.Integer(), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('mal_id')
    )
    op.create_table('staff_page_update',
    sa.Column('mal_id', sa.Integer(), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('mal_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('staff_page_update')
    op.drop_table('people_page_update')
    # ### end Alembic commands ###
