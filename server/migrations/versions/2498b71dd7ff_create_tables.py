"""create tables

Revision ID: 2498b71dd7ff
Revises: 
Create Date: 2023-07-02 15:13:29.973000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2498b71dd7ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('_password_hash', sa.String(), nullable=True),
    sa.Column('admin', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('butterflies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_butterflies_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('genus_species', sa.String(), nullable=False),
    sa.Column('growing_zone', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_plants_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('butterfly_tags',
    sa.Column('butterfly_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['butterfly_id'], ['butterflies.id'], name=op.f('fk_butterfly_tags_butterfly_id_butterflies')),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name=op.f('fk_butterfly_tags_tag_id_tags'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('butterfly_tags')
    op.drop_table('plants')
    op.drop_table('butterflies')
    op.drop_table('users')
    op.drop_table('tags')
    # ### end Alembic commands ###
