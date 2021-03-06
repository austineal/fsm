"""adding tsa info for students

Revision ID: 28e461a1914d
Revises: 31aa32b00865
Create Date: 2015-09-13 13:22:31.649251

"""

# revision identifiers, used by Alembic.
revision = '28e461a1914d'
down_revision = '31aa32b00865'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tsa_docs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doc_name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'students', sa.Column('tsa_eligibility_confirmed', sa.Boolean(), nullable=True))
    op.add_column(u'students', sa.Column('tsa_eligibility_doc', sa.Integer(), nullable=True))
    op.add_column(u'students', sa.Column('tsa_eligibility_doc_id', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'students', 'tsa_eligibility_doc_id')
    op.drop_column(u'students', 'tsa_eligibility_doc')
    op.drop_column(u'students', 'tsa_eligibility_confirmed')
    op.drop_table('tsa_docs')
    ### end Alembic commands ###
