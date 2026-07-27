"""
Migración para agregar sistema de campañas
"""
from alembic import op
import sqlalchemy as sa


def upgrade():
    # Crear tabla de campañas
    op.create_table(
        'campanas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('codigo', sa.String(50), unique=True, nullable=False),
        sa.Column('nombre', sa.String(200), nullable=False),
        sa.Column('descripcion', sa.Text()),
        sa.Column('fecha_inicio', sa.Date()),
        sa.Column('fecha_fin', sa.Date()),
        sa.Column('color_primario', sa.String(7), default='#1e3c72'),
        sa.Column('color_secundario', sa.String(7), default='#2a5298'),
        sa.Column('logo_url', sa.String(500)),
        sa.Column('es_candidato_unico', sa.Boolean(), default=False),
        sa.Column('es_partido_completo', sa.Boolean(), default=False),
        sa.Column('activa', sa.Boolean(), default=False),
        sa.Column('completada', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'))
    )
    
    # Crear tabla de configuración de temas
    op.create_table(
        'configuracion_temas',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('aplica_a_rol', sa.String(50)),
        sa.Column('aplica_a_tipo_eleccion_id', sa.Integer(), sa.ForeignKey('tipos_eleccion.id')),
        sa.Column('campana_id', sa.Integer(), sa.ForeignKey('campanas.id')),
        sa.Column('color_primario', sa.String(7), default='#1e3c72'),
        sa.Column('color_secundario', sa.String(7), default='#2a5298'),
        sa.Column('color_acento', sa.String(7), default='#28a745'),
        sa.Column('color_fondo', sa.String(7), default='#f8f9fa'),
        sa.Column('color_texto', sa.String(7), default='#212529'),
        sa.Column('logo_url', sa.String(500)),
        sa.Column('favicon_url', sa.String(500)),
        sa.Column('activo', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime())
    )
    
    # Agregar campo campana_id a tablas principales
    op.add_column('formularios_e14', sa.Column('campana_id', sa.Integer(), sa.ForeignKey('campanas.id')))
    op.add_column('incidentes', sa.Column('campana_id', sa.Integer(), sa.ForeignKey('campanas.id')))
    op.add_column('delitos', sa.Column('campana_id', sa.Integer(), sa.ForeignKey('campanas.id')))
    
    # Crear campaña por defecto
    op.execute("""
        INSERT INTO campanas (codigo, nombre, descripcion, activa, created_at)
        VALUES ('DEFAULT', 'Campaña Principal', 'Campaña por defecto del sistema', TRUE, NOW())
    """)


def downgrade():
    op.drop_column('formularios_e14', 'campana_id')
    op.drop_column('incidentes', 'campana_id')
    op.drop_column('delitos', 'campana_id')
    op.drop_table('configuracion_temas')
    op.drop_table('campanas')
