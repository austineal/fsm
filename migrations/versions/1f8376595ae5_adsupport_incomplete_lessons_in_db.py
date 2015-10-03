"""adsupport incomplete lessons in db

Revision ID: 1f8376595ae5
Revises: 563b43305f06
Create Date: 2015-10-03 14:35:02.047180

"""

# revision identifiers, used by Alembic.
revision = '1f8376595ae5'
down_revision = '563b43305f06'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flights', sa.Column('complete', sa.Boolean(), nullable=True))
    op.add_column('flights', sa.Column('completed_objectives', sa.String(length=32000), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('flights', 'completed_objectives')
    op.drop_column('flights', 'complete')
    ### end Alembic commands ###
