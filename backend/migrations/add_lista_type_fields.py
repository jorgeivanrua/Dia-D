"""
Migración para agregar campos de tipo de lista a TipoEleccion
"""
from alembic import op
import sqlalchemy as sa


def upgrade():
    # Agregar campos a tipos_eleccion
    op.add_column('tipos_eleccion', sa.Column('permite_lista_cerrada', sa.Boolean(), default=True))
    op.add_column('tipos_eleccion', sa.Column('permite_lista_abierta', sa.Boolean(), default=False))
    op.add_column('tipos_eleccion', sa.Column('permite_coaliciones', sa.Boolean(), default=False))
    
    # Agregar campo a candidatos para indicar si es cabeza de lista
    op.add_column('candidatos', sa.Column('es_cabeza_lista', sa.Boolean(), default=False))


def downgrade():
    op.drop_column('tipos_eleccion', 'permite_lista_cerrada')
    op.drop_column('tipos_eleccion', 'permite_lista_abierta')
    op.drop_column('tipos_eleccion', 'permite_coaliciones')
    op.drop_column('candidatos', 'es_cabeza_lista')
