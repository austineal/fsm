"""adding 141 checkout

Revision ID: 320765f2f92
Revises: 49d5d3c6a31c
Create Date: 2015-09-13 18:07:06.866199

"""

# revision identifiers, used by Alembic.
revision = '320765f2f92'
down_revision = '49d5d3c6a31c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instructors', sa.Column('checkout_141', sa.Boolean(), nullable=True))
    op.add_column('instructors', sa.Column('checkout_141_date', sa.Date(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('instructors', 'checkout_141_date')
    op.drop_column('instructors', 'checkout_141')
    ### end Alembic commands ###