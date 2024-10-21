"""Actualizacion todo el modelo

Revision ID: 496716657299
Revises: 
Create Date: 2024-10-19 23:07:26.106782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '496716657299'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contrac',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('contrac_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contrac_id'], ['contrac.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=1024), nullable=True),
    sa.Column('company_id', sa.String(length=36), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('incident',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('modified_date', sa.DateTime(), nullable=True),
    sa.Column('source', sa.String(length=20), nullable=True),
    sa.Column('customer_id', sa.String(length=36), nullable=False),
    sa.Column('analyst_id', sa.String(length=36), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['analyst_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['customer_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('log_incident',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('details', sa.Text(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('users_id', sa.String(length=36), nullable=False),
    sa.Column('incident_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['incident_id'], ['incident.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log_incident')
    op.drop_table('incident')
    op.drop_table('users')
    op.drop_table('company')
    op.drop_table('contrac')
    # ### end Alembic commands ###