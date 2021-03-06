"""empty message

Revision ID: 5956d8a11065
Revises: 56406ff43d
Create Date: 2015-07-05 20:20:41.014929

"""

# revision identifiers, used by Alembic.
revision = '5956d8a11065'
down_revision = '56406ff43d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flight_lessons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flight_lessons')
    ### end Alembic commands ###
