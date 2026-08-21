#!/usr/bin/env python3
"""Script de verificación rápida para arquitectura Flask+PostgreSQL+Dokploy"""
import os
import sys

def verificar_arquitectura():
    """Verifica que todos los componentes estén en su lugar."""
    
    print("=" * 60)
    print("🏗️  VERIFICACIÓN DE ARQUITECTURA DIA-D")
    print("=" * 60)
    
    # 1. Verificar Python files
    print("\n📁 Archivos de la aplicación:")
    backend_files = [
        'backend/app.py',
        'backend/config.py', 
        'backend/database.py',
        'backend/routes/__init__.py'
    ]
    for f in backend_files:
        exists = os.path.exists(f)
        status = "✅" if exists else "❌"
        print(f"  {status} {f}")
    
    # 2. Verificar Docker files
    print("\n🐳 Archivos Docker:")
    docker_files = [
        'docker-compose.yml',
        'Dockerfile',
        'docker-entrypoint.sh'
    ]
    for f in docker_files:
        exists = os.path.exists(f)
        status = "✅" if exists else "❌"
        print(f"  {status} {f}")
    
    # 3. Verificar .env
    print("\n⚙️  Archivos de entorno:")
    env_files = ['.env', '.env.dokploy']
    for f in env_files:
        exists = os.path.exists(f)
        status = "✅" if exists else "❌"
        print(f"  {status} {f}")
    
    # 4. Verificar configuración PostgreSQL
    print("\n🐘 Configuración de Base de Datos:")
    database_url = os.getenv('DATABASE_URL', '')
    has_postgres = database_url.startswith('postgresql://') or database_url.startswith('postgres://')
    has_sqlite = database_url.startswith('sqlite://')
    
    if has_postgres:
        print(f"  ✅ DATABASE_URL configurada para PostgreSQL")
        print(f"     URL: {database_url[:50]}...")
    elif has_sqlite:
        print(f"  ⚠️ DATABASE_URL usa SQLite (desarrollo/testing)")
        print(f"     URL: {database_url}")
    else:
        print(f"  ❌ DATABASE_URL no configurada")
    
    # 4. Verificar secrets
    print("\n🔐 Seguridad:")
    secret_key = os.getenv('SECRET_KEY', '')
    is_default = secret_key in ['dev-secret-key-change-in-production', 'dia-d-production-secret-key-change-immediately']
    
    if not is_default or secret_key:
        print(f"  {'✅' if secret_key and not is_default else '⚠️'} SECRET_KEY configurada")
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN:")
    print("  Arquitectura: Flask API + PostgreSQL + Docker + Dokploy")
    print("  Base de Datos:", "PostgreSQL" if has_postgres else ("SQLite" if has_sqlite else "No configurada"))
    print("  lista para producción:", "✅" if has_postgres else "⚠️ pending")
    print("=" * 60)

if __name__ == '__main__':
    verificar_arquitectura()