"""empty message

Revision ID: aa4667a0a1a4
Revises: 8ada48e44ba7
Create Date: 2021-02-03 01:35:27.959521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa4667a0a1a4'
down_revision = '8ada48e44ba7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('page_status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('page_status',
    sa.Column('mal_id', sa.INTEGER(), nullable=False),
    sa.Column('category', sa.VARCHAR(length=50), nullable=False),
    sa.Column('last_modified', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('mal_id')
    )
    # ### end Alembic commands ###
