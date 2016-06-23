"""initial db struct

Revision ID: 1dba57a5105b
Revises: None
Create Date: 2015-06-22 18:11:33.658703

"""

# revision identifiers, used by Alembic.
revision = '1dba57a5105b'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # commands auto generated by Alembic - please adjust!
    op.create_table(
        'allowed_orgs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('org_id', sa.String(), nullable=True),
        sa.Column('org_info', sa.String(), nullable=True),
        sa.Column('deployments_limit', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('org_id')
    )
    op.create_table(
        'used_orgs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('org_id', sa.String(), nullable=True),
        sa.Column('deployments_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('org_id')
    )
    # end Alembic commands


def downgrade():
    # commands auto generated by Alembic - please adjust!
    op.drop_table('used_orgs')
    op.drop_table('allowed_orgs')
    # end Alembic commands