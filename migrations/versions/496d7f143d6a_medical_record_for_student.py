"""medical record for student

Revision ID: 496d7f143d6a
Revises: 4e1d9d87caea
Create Date: 2015-07-25 17:17:27.869719

"""

# revision identifiers, used by Alembic.
revision = '496d7f143d6a'
down_revision = '4e1d9d87caea'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('medical_expires', sa.Date(), nullable=True))
    op.add_column('students', sa.Column('medical_received', sa.Date(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'medical_received')
    op.drop_column('students', 'medical_expires')
    ### end Alembic commands ###