"""empty message

Revision ID: 78f2fc4dd009
Revises: c6a9f7b2109c
Create Date: 2021-02-08 23:46:51.649451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78f2fc4dd009'
down_revision = 'c6a9f7b2109c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('manga',
    sa.Column('mal_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('title_english', sa.String(length=200), nullable=True),
    sa.Column('title_japanese', sa.String(length=200), nullable=True),
    sa.Column('image_url', sa.String(length=200), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('work_type', sa.String(length=50), nullable=True),
    sa.Column('volumes', sa.Integer(), nullable=True),
    sa.Column('chapters', sa.Integer(), nullable=True),
    sa.Column('publishing', sa.String(length=50), nullable=True),
    sa.Column('published_from', sa.DateTime(), nullable=True),
    sa.Column('published_to', sa.DateTime(), nullable=True),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('scored_by', sa.Integer(), nullable=True),
    sa.Column('popularity', sa.Integer(), nullable=True),
    sa.Column('members', sa.Integer(), nullable=True),
    sa.Column('favorites', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('mal_id')
    )
    op.create_table('manga_author',
    sa.Column('id', sa.String(length=200), nullable=False),
    sa.Column('position', sa.String(length=100), nullable=True),
    sa.Column('author_type', sa.String(length=100), nullable=True),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.Column('manga_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['manga_id'], ['manga.mal_id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['person.mal_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('manga_author')
    op.drop_table('manga')
    # ### end Alembic commands ###