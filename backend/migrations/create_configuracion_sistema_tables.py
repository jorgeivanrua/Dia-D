"""
Migración: Crear tablas de configuración del sistema
Permite personalizar la apariencia del login
"""
from backend.database import db
from backend.models.configuracion_sistema import ConfiguracionSistema, FondoLogin


def upgrade():
    """Crear tablas de configuración"""
    print("Creando tablas de configuración del sistema...")
    
    # Crear tablas
    db.create_all()
    
    # Crear fondo predeterminado (Bandera de Colombia)
    fondo_default = FondoLogin(
        nombre='Bandera de Colombia',
        tipo='gradient',
        color1='#FCD116',
        color2='#003893',
        color3='#CE1126',
        direccion='180deg',
        overlay_color='#FFFFFF',
        overlay_opacity=0.1,
        activo=True,
        predeterminado=True
    )
    
    db.session.add(fondo_default)
    
    # Crear configuraciones iniciales
    configs = [
        ConfiguracionSistema(
            clave='nombre_sistema',
            valor='Sistema Electoral DÍA D',
            tipo='text',
            descripcion='Nombre del sistema'
        ),
        ConfiguracionSistema(
            clave='subtitulo_sistema',
            valor='Formularios E-14 / E-24',
            tipo='text',
            descripcion='Subtítulo del sistema'
        ),
        ConfiguracionSistema(
            clave='departamento',
            valor='Departamento del Caquetá',
            tipo='text',
            descripcion='Departamento del sistema'
        ),
        ConfiguracionSistema(
            clave='logo_url',
            valor='/static/img/logo.png',
            tipo='image',
            descripcion='URL del logo del sistema'
        )
    ]
    
    for config in configs:
        db.session.add(config)
    
    db.session.commit()
    
    print("✅ Tablas de configuración creadas exitosamente")
    print("✅ Fondo predeterminado (Bandera de Colombia) creado")
    print("✅ Configuraciones iniciales creadas")


def downgrade():
    """Eliminar tablas de configuración"""
    print("Eliminando tablas de configuración del sistema...")
    
    db.session.query(FondoLogin).delete()
    db.session.query(ConfiguracionSistema).delete()
    db.session.commit()
    
    # Nota: No eliminamos las tablas físicamente para evitar pérdida de datos
    # Si se necesita, usar: db.drop_table('fondos_login')
    
    print("✅ Datos de configuración eliminados")


if __name__ == '__main__':
    from backend.app import create_app
    
    app = create_app()
    with app.app_context():
        upgrade()
