"""empty message

Revision ID: edf7d155a43b
Revises: 31a636c1ef0d
Create Date: 2016-07-08 11:13:13.483992

"""

# revision identifiers, used by Alembic.
revision = 'edf7d155a43b'
down_revision = '31a636c1ef0d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('limits')
    op.drop_table('tenants')
    op.drop_table('endpoints')
    op.drop_table('approved_plugins')
    op.drop_table('walle_admins')
    op.create_table('approved_plugins',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('source', sa.String(length=255), nullable=True),
    sa.Column('plugin_type', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('endpoints',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('endpoint', sa.String(length=128), nullable=True),
    sa.Column('type', sa.String(length=24), nullable=True),
    sa.Column('version', sa.String(length=16), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('walle_admins',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=16), nullable=True),
    sa.Column('password', sa.String(length=32), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('expire', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tenants',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('tenant_name', sa.String(length=16), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('endpoint_id', sa.String(length=36), nullable=True),
    sa.Column('cloudify_host', sa.String(length=128), nullable=True),
    sa.Column('cloudify_port', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['endpoint_id'], ['endpoints.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('limits',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('tenant_id', sa.String(length=36), nullable=True),
    sa.Column('soft', sa.Integer(), nullable=True),
    sa.Column('hard', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=24), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('limits')
    op.drop_table('tenants')
    op.drop_table('walle_admins')
    op.drop_table('endpoints')
    op.drop_table('approved_plugins')
    op.create_table('endpoints',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('endpoint', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('version', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'endpoints_pkey')
    )
    op.create_table('tenants',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('tenant_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('endpoint_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cloudify_host', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cloudify_port', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('updated_at', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['endpoint_id'], [u'endpoints.id'], name=u'tenants_endpoint_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'tenants_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('limits',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('tenant_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('soft', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('hard', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('value', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('updated_at', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], [u'tenants.id'], name=u'limits_tenant_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'limits_pkey')
    )
    op.create_table('walle_admins',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('expire', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'walle_admins_pkey'),
    sa.UniqueConstraint('name', name=u'walle_admins_name_key')
    )
    op.create_table('approved_plugins',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('source', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('plugin_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name=u'approved_plugins_pkey')
    )
    ### end Alembic commands ###
