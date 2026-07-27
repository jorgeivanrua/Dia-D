-- Migración para agregar el rol 'monitoreo' al constraint
-- SQLite no permite modificar constraints directamente, 
-- así que necesitamos recrear la tabla

-- Paso 1: Crear tabla temporal con el nuevo constraint
CREATE TABLE users_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL CHECK (rol IN (
        'super_admin',
        'admin_departamental',
        'admin_municipal',
        'coordinador_departamental',
        'coordinador_municipal',
        'coordinador_puesto',
        'testigo_electoral',
        'auditor_electoral',
        'monitoreo'
    )),
    ubicacion_id INTEGER,
    activo BOOLEAN DEFAULT 1,
    ultimo_acceso TIMESTAMP,
    intentos_fallidos INTEGER DEFAULT 0,
    bloqueado_hasta TIMESTAMP,
    presencia_verificada BOOLEAN DEFAULT 0,
    presencia_verificada_at TIMESTAMP,
    ultima_latitud FLOAT,
    ultima_longitud FLOAT,
    ultima_geolocalizacion_at TIMESTAMP,
    precision_geolocalizacion FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ubicacion_id) REFERENCES locations(id)
);

-- Paso 2: Copiar datos de la tabla original
INSERT INTO users_new SELECT * FROM users;

-- Paso 3: Eliminar tabla original
DROP TABLE users;

-- Paso 4: Renombrar tabla nueva
ALTER TABLE users_new RENAME TO users;
