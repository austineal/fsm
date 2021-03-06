"""empty message

Revision ID: 29232e09d1db
Revises: 4945f1b0e799
Create Date: 2015-07-19 15:42:44.363154

"""

# revision identifiers, used by Alembic.
revision = '29232e09d1db'
down_revision = '4945f1b0e799'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('testtypes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('test_type', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('instructor_id', sa.Integer(), nullable=True),
    sa.Column('success', sa.Boolean(), nullable=True),
    sa.Column('test_type_id', sa.Integer(), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['instructor_id'], ['instructors.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.ForeignKeyConstraint(['test_type_id'], ['testtypes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('checkrides')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('checkrides',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('date', sa.DATE(), nullable=True),
    sa.Column('student_id', sa.INTEGER(), nullable=True),
    sa.Column('instructor_id', sa.INTEGER(), nullable=True),
    sa.Column('success', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['instructor_id'], [u'instructors.id'], ),
    sa.ForeignKeyConstraint(['student_id'], [u'students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('tests')
    op.drop_table('testtypes')
    ### end Alembic commands ###
