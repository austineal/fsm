"""empty message

Revision ID: 523824fc5654
Revises: 1b8aa0869b8a
Create Date: 2015-07-19 14:44:33.434214

"""

# revision identifiers, used by Alembic.
revision = '523824fc5654'
down_revision = '1b8aa0869b8a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('instructor_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'instructor_id')
    ### end Alembic commands ###
