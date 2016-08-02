"""empty message

Revision ID: edb043051d1d
Revises: edf7d155a43b
Create Date: 2016-08-01 17:52:59.822816

"""

# revision identifiers, used by Alembic.
revision = 'edb043051d1d'
down_revision = 'edf7d155a43b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rights',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tenant_rights',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('tenant_id', sa.String(length=36), nullable=True),
    sa.Column('rights_id', sa.String(length=36), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['rights_id'], ['rights.id'], ),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tenant_rights')
    op.drop_table('rights')
    ### end Alembic commands ###
