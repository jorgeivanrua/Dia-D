#!/usr/bin/env python3
"""
Script para probar el endpoint de puestos con alertas de incidentes y delitos
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
PUESTOS_URL = f"{BASE_URL}/api/locations/puestos-geolocalizados"

def login():
    """Login y obtener token"""
    print("🔐 Iniciando sesión...")
    
    # Credenciales de super admin
    credentials = {
        "email": "admin@sistema.com",
        "password": "admin123"
    }
    
    response = requests.post(LOGIN_URL, json=credentials)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f"✅ Login exitoso")
        return token
    else:
        print(f"❌ Error en login: {response.status_code}")
        print(response.text)
        return None

def obtener_puestos(token):
    """Obtener puestos con alertas"""
    print("\n📍 Obteniendo puestos geolocalizados...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(PUESTOS_URL, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            puestos = data.get('data', [])
            print(f"✅ Se obtuvieron {len(puestos)} puestos")
            return puestos
        else:
            print(f"❌ Error: {data.get('error')}")
            return []
    else:
        print(f"❌ Error HTTP: {response.status_code}")
        print(response.text)
        return []

def analizar_puestos(puestos):
    """Analizar puestos y mostrar estadísticas"""
    print("\n📊 ANÁLISIS DE PUESTOS\n" + "="*60)
    
    total_puestos = len(puestos)
    puestos_con_alertas = 0
    puestos_con_alertas_criticas = 0
    total_incidentes = 0
    total_incidentes_criticos = 0
    total_delitos = 0
    total_delitos_graves = 0
    
    # Contadores por estado de avance
    sin_avance = 0
    en_progreso = 0
    completados = 0
    
    print(f"Total de puestos: {total_puestos}\n")
    
    for puesto in puestos:
        # Contar alertas
        if puesto.get('tiene_alertas'):
            puestos_con_alertas += 1
        if puesto.get('tiene_alertas_criticas'):
            puestos_con_alertas_criticas += 1
        
        total_incidentes += puesto.get('incidentes_activos', 0)
        total_incidentes_criticos += puesto.get('incidentes_criticos', 0)
        total_delitos += puesto.get('delitos_activos', 0)
        total_delitos_graves += puesto.get('delitos_graves', 0)
        
        # Contar por avance
        porcentaje = puesto.get('porcentaje_avance', 0)
        if porcentaje == 0:
            sin_avance += 1
        elif porcentaje >= 100:
            completados += 1
        else:
            en_progreso += 1
    
    print("AVANCE DE FORMULARIOS E-14:")
    print(f"  🔴 Sin avance (0%):        {sin_avance} puestos")
    print(f"  🟡 En progreso (1-99%):    {en_progreso} puestos")
    print(f"  🟢 Completados (100%):     {completados} puestos")
    
    print("\nALERTAS:")
    print(f"  ⚠️  Puestos con alertas:           {puestos_con_alertas}")
    print(f"  🚨 Puestos con alertas críticas:  {puestos_con_alertas_criticas}")
    
    print("\nINCIDENTES:")
    print(f"  📋 Total incidentes activos:      {total_incidentes}")
    print(f"  ⚠️  Incidentes críticos:           {total_incidentes_criticos}")
    
    print("\nDELITOS:")
    print(f"  🚨 Total delitos activos:         {total_delitos}")
    print(f"  ⚠️  Delitos graves:                {total_delitos_graves}")
    
    # Mostrar puestos con alertas críticas
    if puestos_con_alertas_criticas > 0:
        print("\n" + "="*60)
        print("🚨 PUESTOS CON ALERTAS CRÍTICAS:")
        print("="*60)
        
        for puesto in puestos:
            if puesto.get('tiene_alertas_criticas'):
                print(f"\n📍 {puesto['puesto_nombre']} (Código: {puesto['puesto_codigo']})")
                print(f"   Municipio: {puesto['municipio_nombre']}")
                print(f"   Departamento: {puesto['departamento_nombre']}")
                
                if puesto.get('incidentes_criticos', 0) > 0:
                    print(f"   ⚠️  Incidentes críticos: {puesto['incidentes_criticos']}")
                
                if puesto.get('delitos_graves', 0) > 0:
                    print(f"   🚨 Delitos graves: {puesto['delitos_graves']}")
                
                print(f"   📊 Avance E-14: {puesto['porcentaje_avance']}%")
    
    # Mostrar algunos ejemplos de puestos
    print("\n" + "="*60)
    print("📋 EJEMPLOS DE PUESTOS (primeros 5):")
    print("="*60)
    
    for i, puesto in enumerate(puestos[:5], 1):
        print(f"\n{i}. {puesto['puesto_nombre']} (Código: {puesto['puesto_codigo']})")
        print(f"   📍 Ubicación: {puesto['municipio_nombre']}, {puesto['departamento_nombre']}")
        print(f"   🗳️  Mesas: {puesto['total_mesas']}")
        print(f"   📋 E-14 recibidos: {puesto['total_formularios']}")
        print(f"   ✅ E-14 validados: {puesto['formularios_validados']}")
        print(f"   📊 Avance: {puesto['porcentaje_avance']}%")
        
        if puesto.get('tiene_alertas'):
            print(f"   ⚠️  Incidentes: {puesto['incidentes_activos']} (críticos: {puesto['incidentes_criticos']})")
            print(f"   🚨 Delitos: {puesto['delitos_activos']} (graves: {puesto['delitos_graves']})")

def main():
    """Función principal"""
    print("="*60)
    print("TEST: PUESTOS CON ALERTAS DE INCIDENTES Y DELITOS")
    print("="*60)
    
    # Login
    token = login()
    if not token:
        print("\n❌ No se pudo obtener el token de autenticación")
        return
    
    # Obtener puestos
    puestos = obtener_puestos(token)
    if not puestos:
        print("\n⚠️  No se obtuvieron puestos")
        return
    
    # Analizar puestos
    analizar_puestos(puestos)
    
    print("\n" + "="*60)
    print("✅ Test completado")
    print("="*60)

if __name__ == "__main__":
    main()
