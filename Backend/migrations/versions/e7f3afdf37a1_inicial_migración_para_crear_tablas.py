"""Inicial migración para crear tablas

Revision ID: e7f3afdf37a1
Revises: 
Create Date: 2024-10-17 21:06:40.984969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7f3afdf37a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Crear la tabla contrato primero
    op.create_table(
        'contrato',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('descripcion', sa.String(length=200), nullable=False),
        sa.Column('fecha_inicio', sa.Date(), nullable=False),
        sa.Column('fecha_fin', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Crear la tabla empresa después
    op.create_table(
        'empresa',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('contrato_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['contrato_id'], ['contrato.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )

    # Crear la tabla user, si no se ha creado aún
    op.create_table(
        'user',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('password_hash', sa.String(length=1024), nullable=True),
        sa.Column('empresa_id', sa.String(length=36), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(['empresa_id'], ['empresa.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )


#