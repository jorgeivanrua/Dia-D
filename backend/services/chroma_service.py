"""
Servicio mínimo para conectar con ChromaDB (local o persistente)
"""
from typing import Optional
import os

try:
    import chromadb
    from chromadb.config import Settings
except Exception:
    chromadb = None


class ChromaService:
    """Wrapper simple para inicializar cliente Chroma si está disponible"""

    client = None

    @staticmethod
    def init_client():
        if ChromaService.client is not None:
            return ChromaService.client

        if chromadb is None:
            print("Chroma no está instalado — deshabilitado")
            return None

        persist_dir = os.environ.get('CHROMA_PERSIST_DIR', 'chroma_db')
        server_host = os.environ.get('CHROMA_SERVER_HOST', '')
        server_port = int(os.environ.get('CHROMA_SERVER_PORT', 8000) or 8000)

        try:
            if server_host:
                # Intentar conexión a Chroma Server (Http client)
                try:
                    from chromadb.utils import embedding_functions
                    # The chromadb Http client is available in newer releases
                    client = chromadb.HttpClient(host=server_host, port=server_port)
                    ChromaService.client = client
                    return client
                except Exception:
                    # Fall back to embedded
                    pass

            # Embedded (persist to duckdb+parquet)
            settings = Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_dir)
            client = chromadb.Client(settings)
            ChromaService.client = client
            return client

        except Exception as e:
            print(f"No se pudo inicializar Chroma: {e}")
            return None


# Inicializar automáticamente si está configurado
if os.environ.get('CHROMA_ENABLED', 'False') == 'True':
    ChromaService.init_client()
