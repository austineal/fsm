"""empty message

Revision ID: abd909c94c4
Revises: 4c49ee321fa8
Create Date: 2015-07-19 16:07:00.080585

"""

# revision identifiers, used by Alembic.
revision = 'abd909c94c4'
down_revision = '4c49ee321fa8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    pass
    ### commands auto generated by Alembic - please adjust! ###
    #op.drop_column('testtypes', 'name')
    ### end Alembic commands ###


def downgrade():
    pass
    ### commands auto generated by Alembic - please adjust! ###
    #op.add_column('testtypes', sa.Column('name', sa.VARCHAR(length=32), nullable=True))
    ### end Alembic commands ###
