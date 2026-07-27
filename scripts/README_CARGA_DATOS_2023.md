# Carga de Datos Electorales 2023

## Scripts Creados

### 1. `cargar_partidos_2023.py`
Carga los partidos políticos que participaron en las elecciones regionales de 2023.

**Partidos incluidos:**
- Pacto Histórico
- Partido Liberal Colombiano
- Partido Conservador Colombiano
- Alianza Verde
- Centro Democrático
- Cambio Radical
- Partido de la U
- MIRA (Movimiento Independiente de Renovación Absoluta)
- Comunes
- ASI (Alianza Social Independiente)
- Colombia Renaciente (Dignidad)
- Nuevo Liberalismo
- Voto en Blanco

**Características:**
- Incluye logos oficiales de Wikipedia
- Colores representativos de cada partido
- Orden de visualización configurado
- Actualiza partidos existentes o crea nuevos

**Uso:**
```bash
python scripts/cargar_partidos_2023.py
```

### 2. `cargar_candidatos_2023.py`
Carga candidatos principales de las elecciones regionales 2023.

**Candidatos incluidos:**

**Bogotá - Alcaldía:**
- Carlos Fernando Galán (Nuevo Liberalismo)
- Juan Daniel Oviedo (Pacto Histórico)
- Rodrigo Lara (Alianza Verde)

**Cundinamarca - Gobernación:**
- Jorge Emilio Rey (Partido Liberal)
- Nicolás García (Partido Conservador)

**Antioquia - Gobernación:**
- Andrés Julián Rendón (Centro Democrático)
- Juan Carlos Upegui (Partido Liberal)

**Valle del Cauca - Gobernación:**
- Dilian Francisca Toro (Partido Conservador)

**Características:**
- Códigos únicos por candidato
- Asociación con partido y tipo de elección
- Marcados como cabeza de lista
- Número de lista asignado

**Uso:**
```bash
python scripts/cargar_candidatos_2023.py
```

## Orden de Ejecución

1. Primero ejecutar `cargar_partidos_2023.py` para crear los partidos
2. Luego ejecutar `cargar_candidatos_2023.py` para crear los candidatos

## Notas

- Los scripts son idempotentes: pueden ejecutarse múltiples veces sin duplicar datos
- Si un partido o candidato ya existe (por código), se actualiza en lugar de crear uno nuevo
- Los logos están alojados en Wikipedia para garantizar disponibilidad
- Los datos son de ejemplo y pueden ser extendidos según necesidades

## Próximos Pasos

Para agregar más datos:
1. Editar los arrays `partidos_2023` o `candidatos_data` en los scripts
2. Ejecutar nuevamente los scripts
3. Los datos se actualizarán automáticamente
