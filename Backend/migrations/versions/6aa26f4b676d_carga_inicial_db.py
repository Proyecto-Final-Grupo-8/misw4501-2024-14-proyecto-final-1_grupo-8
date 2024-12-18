"""Carga Inicial db

Revision ID: 6aa26f4b676d
Revises: 
Create Date: 2024-11-03 14:33:42.468145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6aa26f4b676d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('company_services',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('id_company', sa.String(length=36), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['id_company'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contract',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('plan', sa.String(length=20), nullable=False),
    sa.Column('company_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=1024), nullable=True),
    sa.Column('company_id', sa.String(length=36), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('incident',
    sa.Column('id', sa.String(length=36), nullable=False),
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
    op.create_table('invoices',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('id_contract', sa.String(length=36), nullable=False),
    sa.Column('company_id', sa.String(length=36), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['id_contract'], ['contract.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rates',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.Column('rate_per_incident', sa.Float(), nullable=False),
    sa.Column('id_contract', sa.String(length=36), nullable=False),
    sa.Column('source', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['id_contract'], ['contract.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('log_incident',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('details', sa.Text(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('users_id', sa.String(length=36), nullable=False),
    sa.Column('incident_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['incident_id'], ['incident.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('log_invoices',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('id_invoice', sa.String(length=36), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('source', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['id_invoice'], ['invoices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log_invoices')
    op.drop_table('log_incident')
    op.drop_table('rates')
    op.drop_table('invoices')
    op.drop_table('incident')
    op.drop_table('users')
    op.drop_table('contract')
    op.drop_table('company_services')
    op.drop_table('company')
    # ### end Alembic commands ###
