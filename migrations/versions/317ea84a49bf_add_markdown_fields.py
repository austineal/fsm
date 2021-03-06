"""add markdown fields

Revision ID: 317ea84a49bf
Revises: 218b9548fd64
Create Date: 2015-08-23 22:36:50.988174

"""

# revision identifiers, used by Alembic.
revision = '317ea84a49bf'
down_revision = '218b9548fd64'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flight_lessons', sa.Column('completion_standards_html', sa.String(length=1024), nullable=True))
    op.add_column('flight_lessons', sa.Column('objectives_html', sa.String(length=1024), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('flight_lessons', 'objectives_html')
    op.drop_column('flight_lessons', 'completion_standards_html')
    ### end Alembic commands ###
