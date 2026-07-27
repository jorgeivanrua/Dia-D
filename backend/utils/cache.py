"""
Sistema de caché simple para optimizar consultas frecuentes
Usa memoria local (puede migrar a Redis en producción)
"""
from functools import wraps
from datetime import datetime, timedelta
import json
import hashlib


class SimpleCache:
    """Caché simple en memoria"""
    
    def __init__(self):
        self._cache = {}
        self._timestamps = {}
    
    def get(self, key):
        """Obtener valor del caché"""
        if key in self._cache:
            timestamp = self._timestamps.get(key)
            if timestamp and datetime.now() < timestamp:
                return self._cache[key]
            else:
                # Expiró, eliminar
                self.delete(key)
        return None
    
    def set(self, key, value, timeout=60):
        """Guardar valor en caché con timeout en segundos"""
        self._cache[key] = value
        self._timestamps[key] = datetime.now() + timedelta(seconds=timeout)
    
    def delete(self, key):
        """Eliminar valor del caché"""
        if key in self._cache:
            del self._cache[key]
        if key in self._timestamps:
            del self._timestamps[key]
    
    def clear(self):
        """Limpiar todo el caché"""
        self._cache.clear()
        self._timestamps.clear()
    
    def cleanup(self):
        """Limpiar entradas expiradas"""
        now = datetime.now()
        expired_keys = [
            key for key, timestamp in self._timestamps.items()
            if timestamp < now
        ]
        for key in expired_keys:
            self.delete(key)


# Instancia global del caché
cache = SimpleCache()


def cache_result(timeout=60, key_prefix=''):
    """
    Decorador para cachear resultados de funciones
    
    Args:
        timeout: Tiempo en segundos que el resultado permanece en caché
        key_prefix: Prefijo para la clave del caché
    
    Ejemplo:
        @cache_result(timeout=30, key_prefix='stats')
        def get_estadisticas():
            return calcular_estadisticas()
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generar clave única basada en función y argumentos
            cache_key = _generate_cache_key(f.__name__, args, kwargs, key_prefix)
            
            # Intentar obtener del caché
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Si no está en caché, ejecutar función
            result = f(*args, **kwargs)
            
            # Guardar en caché
            cache.set(cache_key, result, timeout)
            
            return result
        
        # Agregar método para limpiar caché de esta función
        decorated_function.clear_cache = lambda: _clear_function_cache(f.__name__, key_prefix)
        
        return decorated_function
    return decorator


def _generate_cache_key(func_name, args, kwargs, prefix=''):
    """Generar clave única para el caché"""
    # Convertir args y kwargs a string
    args_str = str(args) + str(sorted(kwargs.items()))
    
    # Generar hash
    hash_obj = hashlib.md5(args_str.encode())
    hash_str = hash_obj.hexdigest()[:8]
    
    # Construir clave
    if prefix:
        return f"{prefix}:{func_name}:{hash_str}"
    return f"{func_name}:{hash_str}"


def _clear_function_cache(func_name, prefix=''):
    """Limpiar caché de una función específica"""
    pattern = f"{prefix}:{func_name}:" if prefix else f"{func_name}:"
    keys_to_delete = [
        key for key in cache._cache.keys()
        if key.startswith(pattern)
    ]
    for key in keys_to_delete:
        cache.delete(key)


def invalidate_cache(patterns=None):
    """
    Invalidar caché por patrones
    
    Args:
        patterns: Lista de patrones a invalidar (ej: ['stats:', 'users:'])
                 Si es None, limpia todo el caché
    """
    if patterns is None:
        cache.clear()
        return
    
    for pattern in patterns:
        keys_to_delete = [
            key for key in cache._cache.keys()
            if pattern in key
        ]
        for key in keys_to_delete:
            cache.delete(key)


# Tarea de limpieza periódica (ejecutar cada 5 minutos)
def cleanup_expired_cache():
    """Limpiar entradas expiradas del caché"""
    cache.cleanup()


# ============================================================================
# DECORADORES ESPECÍFICOS PARA MONITOREO
# ============================================================================

def cache_monitoreo(timeout=30):
    """Caché específico para endpoints de monitoreo (30 segundos por defecto)"""
    return cache_result(timeout=timeout, key_prefix='monitoreo')


def cache_estadisticas(timeout=60):
    """Caché para estadísticas generales (1 minuto)"""
    return cache_result(timeout=timeout, key_prefix='stats')


def cache_ubicaciones(timeout=300):
    """Caché para ubicaciones (5 minutos, cambian poco)"""
    return cache_result(timeout=timeout, key_prefix='locations')


# ============================================================================
# UTILIDADES
# ============================================================================

def get_cache_stats():
    """Obtener estadísticas del caché"""
    now = datetime.now()
    total_entries = len(cache._cache)
    expired_entries = sum(
        1 for timestamp in cache._timestamps.values()
        if timestamp < now
    )
    active_entries = total_entries - expired_entries
    
    return {
        'total_entries': total_entries,
        'active_entries': active_entries,
        'expired_entries': expired_entries,
        'cache_keys': list(cache._cache.keys())
    }


def warm_cache():
    """Pre-cargar caché con datos frecuentes (opcional)"""
    # Implementar según necesidades
    pass
