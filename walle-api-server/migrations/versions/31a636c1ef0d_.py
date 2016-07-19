"""empty message

Revision ID: 31a636c1ef0d
Revises: f2e8db06c206
Create Date: 2016-07-06 12:50:37.999593

"""

# revision identifiers, used by Alembic.
revision = '31a636c1ef0d'
down_revision = 'f2e8db06c206'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('endpoints',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('endpoint', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tenants',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('tenant_name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('endpoint_id', sa.String(), nullable=True),
    sa.Column('cloudify_host', sa.String(), nullable=True),
    sa.Column('cloudify_port', sa.String(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.Column('updated_at', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['endpoint_id'], ['endpoints.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('limits',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('tenant_id', sa.String(), nullable=True),
    sa.Column('soft', sa.Integer(), nullable=True),
    sa.Column('hard', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('created_at', sa.String(), nullable=True),
    sa.Column('updated_at', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('service_url_to_cloudify_with_limits')
    op.drop_table('allowed_service_urls')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('allowed_service_urls',
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('service_url', sa.VARCHAR(), nullable=True),
    sa.Column('tenant', sa.VARCHAR(), nullable=True),
    sa.Column('info', sa.VARCHAR(), nullable=True),
    sa.Column('created_at', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('service_url_to_cloudify_with_limits',
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('deployment_limits', sa.INTEGER(), nullable=True),
    sa.Column('number_of_deployments', sa.INTEGER(), nullable=True),
    sa.Column('cloudify_host', sa.VARCHAR(), nullable=True),
    sa.Column('cloudify_port', sa.VARCHAR(), nullable=True),
    sa.Column('created_at', sa.VARCHAR(), nullable=True),
    sa.Column('updated_at', sa.VARCHAR(), nullable=True),
    sa.Column('serviceurl_id', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['serviceurl_id'], [u'allowed_service_urls.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('limits')
    op.drop_table('tenants')
    op.drop_table('endpoints')
    ### end Alembic commands ###