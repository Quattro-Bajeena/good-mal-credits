"""merge page updates into one table

Revision ID: 8ada48e44ba7
Revises: 4944ac794689
Create Date: 2021-02-03 01:34:22.050243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ada48e44ba7'
down_revision = '4944ac794689'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('page_status',
    sa.Column('mal_id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('mal_id')
    )
    op.drop_table('people_page_update')
    op.drop_table('staff_page_update')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('staff_page_update',
    sa.Column('mal_id', sa.INTEGER(), nullable=False),
    sa.Column('last_modified', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('mal_id')
    )
    op.create_table('people_page_update',
    sa.Column('mal_id', sa.INTEGER(), nullable=False),
    sa.Column('last_modified', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('mal_id')
    )
    op.drop_table('page_status')
    # ### end Alembic commands ###