"""empty message

Revision ID: d2e3af356ee
Revises: e9ab5cb3e2c
Create Date: 2015-07-19 13:18:16.176201

"""

# revision identifiers, used by Alembic.
revision = 'd2e3af356ee'
down_revision = 'e9ab5cb3e2c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('studenttypes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_type', sa.String(length=8), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('enrollments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'students', sa.Column('student_type_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'students', 'student_type_id')
    op.drop_table('enrollments')
    op.drop_table('studenttypes')
    ### end Alembic commands ###
