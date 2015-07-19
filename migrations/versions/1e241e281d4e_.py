"""empty message

Revision ID: 1e241e281d4e
Revises: d2e3af356ee
Create Date: 2015-07-19 13:35:52.632410

"""

# revision identifiers, used by Alembic.
revision = '1e241e281d4e'
down_revision = 'd2e3af356ee'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('enrollments')
    op.add_column('students', sa.Column('enrollment_end_date', sa.Date(), nullable=True))
    op.add_column('students', sa.Column('enrollment_start_date', sa.Date(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'enrollment_start_date')
    op.drop_column('students', 'enrollment_end_date')
    op.create_table('enrollments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('student_id', sa.INTEGER(), nullable=True),
    sa.Column('start_date', sa.DATE(), nullable=True),
    sa.Column('end_date', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], [u'students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###