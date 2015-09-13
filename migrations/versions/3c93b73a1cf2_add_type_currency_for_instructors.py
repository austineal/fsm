"""add type currency for instructors

Revision ID: 3c93b73a1cf2
Revises: 320765f2f92
Create Date: 2015-09-13 18:23:48.441951

"""

# revision identifiers, used by Alembic.
revision = '3c93b73a1cf2'
down_revision = '320765f2f92'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instructors', sa.Column('me_currency_end_date', sa.Date(), nullable=True))
    op.add_column('instructors', sa.Column('me_currency_start_date', sa.Date(), nullable=True))
    op.add_column('instructors', sa.Column('night_currency_end_date', sa.Date(), nullable=True))
    op.add_column('instructors', sa.Column('night_currency_start_date', sa.Date(), nullable=True))
    op.add_column('instructors', sa.Column('tailwheel_currency_end_date', sa.Date(), nullable=True))
    op.add_column('instructors', sa.Column('tailwheel_currency_start_date', sa.Date(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('instructors', 'tailwheel_currency_start_date')
    op.drop_column('instructors', 'tailwheel_currency_end_date')
    op.drop_column('instructors', 'night_currency_start_date')
    op.drop_column('instructors', 'night_currency_end_date')
    op.drop_column('instructors', 'me_currency_start_date')
    op.drop_column('instructors', 'me_currency_end_date')
    ### end Alembic commands ###
