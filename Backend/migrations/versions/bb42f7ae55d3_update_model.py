"""Update Model

Revision ID: bb42f7ae55d3
Revises: 17f08b30d97d
Create Date: 2024-10-22 20:29:47.622306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb42f7ae55d3'
down_revision = '17f08b30d97d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###
