# Tipos de Elecciones en Colombia

## Descripción
En Colombia existen diferentes tipos de elecciones según el cargo a elegir. Cada tipo tiene características específicas sobre cómo se votan y cómo se cuentan los votos.

---

## 1. Clasificación de Elecciones

### 1.1 Elecciones Uninominales
**Definición**: Se elige a **una sola persona** para el cargo.

**Características**:
- ✅ Se vota por **un candidato específico**
- ✅ Gana quien obtenga **más votos**
- ✅ No hay listas de partido
- ✅ Cada candidato puede tener o no partido

**Tipos de elecciones uninominales**:

#### A. Presidencia y Vicepresidencia
- **Nivel**: Nacional
- **Votación**: Todo el país vota el mismo día
- **Fórmula**: Presidente + Vicepresidente (binomio)
- **Ganador**: Mayoría absoluta (50% + 1) o segunda vuelta
- **Duración**: 4 años

**En el sistema**:
```python
tipo_eleccion = TipoEleccion(
    codigo='PRES',
    nombre='Presidencia y Vicepresidencia',
    es_uninominal=True,
    permite_lista_cerrada=False,
    permite_lista_abierta=False
)
```

**Formulario E-14**:
- Se registran votos por **candidato** (binomio)
- No se registran votos por partido
- Ejemplo: "Gustavo Petro - Francia Márquez"

#### B. Gobernación
- **Nivel**: Departamental
- **Votación**: Solo votantes del departamento
- **Ganador**: Mayoría simple (más votos)
- **Duración**: 4 años

**En el sistema**:
```python
tipo_eleccion = TipoEleccion(
    codigo='GOB',
    nombre='Gobernación',
    es_uninominal=True,
    permite_lista_cerrada=False,
    permite_lista_abierta=False
)
```

#### C. Alcaldía
- **Nivel**: Municipal
- **Votación**: Solo votantes del municipio
- **Ganador**: Mayoría simple (más votos)
- **Duración**: 4 años

**En el sistema**:
```python
tipo_eleccion = TipoEleccion(
    codigo='ALC',
    nombre='Alcaldía',
    es_uninominal=True,
    permite_lista_cerrada=False,
    permite_lista_abierta=False
)
```

---

### 1.2 Elecciones de Corporaciones Públicas (Listas)
**Definición**: Se eligen **múltiples personas** para conformar una corporación.

**Características**:
- ✅ Se vota por **partido** o **candidato dentro del partido**
- ✅ Los partidos presentan **listas de candidatos**
- ✅ Se reparten curules según votos obtenidos
- ✅ Sistema de **cifra repartidora** (D'Hondt)

**Tipos de listas**:

#### Lista Cerrada
- El votante vota por el **partido**
- No puede elegir candidatos específicos
- El orden de la lista lo define el partido
- Los elegidos son los primeros de la lista según curules obtenidas

#### Lista Abierta (Voto Preferente)
- El votante puede votar por el **partido** o por un **candidato específico**
- Si vota por candidato, ese voto cuenta para el partido Y para el candidato
- Los candidatos más votados dentro del partido son elegidos
- Permite reordenar la lista según preferencias de votantes

---

### 1.3 Tipos de Corporaciones Públicas

#### A. Senado de la República
- **Nivel**: Nacional
- **Votación**: Todo el país (circunscripción nacional)
- **Curules**: 100 senadores (+ 5 especiales)
- **Tipo de lista**: Abierta (voto preferente)
- **Duración**: 4 años

**Características especiales**:
- Circunscripción nacional (se vota en todo el país)
- 100 curules ordinarias
- 2 curules para comunidades indígenas
- 2 curules para comunidades afrocolombianas
- 1 curul para colombianos en el exterior

**En el sistema**:
```python
tipo_eleccion = TipoEleccion(
    codigo='SEN',
    nombre='Senado de la República',
    es_uninominal=False,
    permite_lista_cerrada=True,
    permite_lista_abierta=True,  # Voto preferente
    permite_coaliciones=True
)
```

**Formulario E-14**:
- Se registran votos por **partido**
- Se registran votos por **candidato** (voto preferente)
- Ejemplo:
  - Partido Liberal: 150 votos
  - Candidato Juan Pérez (Liberal): 80 votos
  - Candidato María García (Liberal): 70 votos

#### B. Cámara de Representantes
- **Nivel**: Departamental (circunscripciones territoriales)
- **Votación**: Por departamento
- **Curules**: Variable según población del departamento
- **Tipo de lista**: Abierta (voto preferente)
- **Duración**: 4 años

**Características especiales**:
- Cada departamento es una circunscripción
- Número de curules según población
- Mínimo 2 representantes por departamento
- Circunscripciones especiales (indígenas, afro, etc.)

**En el sistema**:
```python
tipo_eleccion = TipoEleccion(
    codigo='CAM',
    nombre='Cámara de Representantes',
    es_uninominal=False,
    permite_lista_cerrada=True,
    permite_lista_abierta=True,
    permite_coaliciones=True
)
```

#### C. Asamblea Departamental
- **Nivel**: Departamental
- **Votación**: Solo votantes del departamento
- **Curules**: Variable según población (11-31 diputados)
- **Tipo de lista**: Abierta (voto preferente)
- **Duración**: 4 años

**En el sistema**:
```python
tipo_eleccion = TipoEleccion(
    codigo='ASA',
    nombre='Asamblea Departamental',
    es_uninominal=False,
    permite_lista_cerrada=True,
    permite_lista_abierta=True,
    permite_coaliciones=True
)
```

#### D. Concejo Municipal
- **Nivel**: Municipal
- **Votación**: Solo votantes del municipio
- **Curules**: Variable según población (7-21 concejales)
- **Tipo de lista**: Abierta (voto preferente)
- **Duración**: 4 años

**En el sistema**:
```python
tipo_eleccion = TipoEleccion(
    codigo='CON',
    nombre='Concejo Municipal',
    es_uninominal=False,
    permite_lista_cerrada=True,
    permite_lista_abierta=True,
    permite_coaliciones=True
)
```

#### E. Juntas Administradoras Locales (JAL)
- **Nivel**: Local (comunas o corregimientos)
- **Votación**: Solo votantes de la localidad
- **Curules**: Variable (5-9 ediles)
- **Tipo de lista**: Abierta
- **Duración**: 4 años

---

## 2. Cómo se Registran los Votos

### 2.1 Elecciones Uninominales (Presidencia, Gobernación, Alcaldía)

**En el Formulario E-14**:
```javascript
// Solo se registran votos por candidato
{
  "tipo_eleccion_id": 1,  // Presidencia
  "votos_candidatos": [
    {
      "candidato_id": 1,  // Gustavo Petro
      "votos": 250
    },
    {
      "candidato_id": 2,  // Rodolfo Hernández
      "votos": 180
    }
  ],
  "votos_nulos": 15,
  "votos_blancos": 10
}
```

**NO se registran votos por partido** en elecciones uninominales.

### 2.2 Elecciones de Corporaciones (Senado, Cámara, Asamblea, Concejo)

**En el Formulario E-14**:
```javascript
// Se registran votos por partido Y por candidato
{
  "tipo_eleccion_id": 2,  // Senado
  "votos_partidos": [
    {
      "partido_id": 1,  // Partido Liberal
      "votos": 300  // Votos totales del partido
    },
    {
      "partido_id": 2,  // Partido Conservador
      "votos": 250
    }
  ],
  "votos_candidatos": [
    {
      "candidato_id": 10,  // Juan Pérez (Liberal)
      "votos": 150  // Voto preferente
    },
    {
      "candidato_id": 11,  // María García (Liberal)
      "votos": 100
    },
    {
      "candidato_id": 20,  // Pedro López (Conservador)
      "votos": 120
    }
  ],
  "votos_nulos": 20,
  "votos_blancos": 15
}
```

**Importante**:
- Los votos por candidato **también cuentan para el partido**
- Si un votante marca candidato, ese voto suma al partido
- Si un votante marca solo partido, ese voto NO se asigna a ningún candidato específico

---

## 3. Sistema de Asignación de Curules

### 3.1 Cifra Repartidora (Método D'Hondt)

**Para corporaciones públicas** (Senado, Cámara, Asamblea, Concejo):

**Paso 1**: Sumar votos totales por partido
```
Partido Liberal: 10,000 votos
Partido Conservador: 8,000 votos
Centro Democrático: 6,000 votos
```

**Paso 2**: Calcular umbral (3% de votos válidos)
```
Total votos válidos: 24,000
Umbral (3%): 720 votos
```

**Paso 3**: Aplicar cifra repartidora
```
Curules a repartir: 10

División sucesiva:
Partido Liberal:    10000/1=10000, 10000/2=5000, 10000/3=3333, ...
Partido Conservador: 8000/1=8000,  8000/2=4000,  8000/3=2666, ...
Centro Democrático:  6000/1=6000,  6000/2=3000,  6000/3=2000, ...

Ordenar de mayor a menor y asignar curules:
1. Liberal: 10000 → Curul 1
2. Conservador: 8000 → Curul 2
3. Centro Democrático: 6000 → Curul 3
4. Liberal: 5000 → Curul 4
5. Conservador: 4000 → Curul 5
6. Liberal: 3333 → Curul 6
7. Centro Democrático: 3000 → Curul 7
8. Conservador: 2666 → Curul 8
9. Liberal: 2500 → Curul 9
10. Centro Democrático: 2000 → Curul 10

Resultado:
- Partido Liberal: 4 curules
- Partido Conservador: 3 curules
- Centro Democrático: 3 curules
```

**Paso 4**: Asignar candidatos dentro de cada partido
```
Partido Liberal (4 curules):
- Si es lista cerrada: Los primeros 4 de la lista
- Si es lista abierta: Los 4 candidatos más votados

Candidatos del Partido Liberal:
1. Juan Pérez: 2,500 votos → Elegido
2. María García: 2,000 votos → Elegido
3. Pedro Martínez: 1,800 votos → Elegido
4. Ana López: 1,500 votos → Elegido
5. Carlos Rodríguez: 1,200 votos → No elegido
```

---

## 4. Configuración en el Sistema

### 4.1 Crear Tipo de Elección

```python
# Ejemplo: Senado
senado = TipoEleccion(
    codigo='SEN',
    nombre='Senado de la República',
    descripcion='Elección de 100 senadores',
    es_uninominal=False,  # Es corporación
    permite_lista_cerrada=True,
    permite_lista_abierta=True,  # Voto preferente
    permite_coaliciones=True,
    activo=True,
    orden=1
)

# Ejemplo: Presidencia
presidencia = TipoEleccion(
    codigo='PRES',
    nombre='Presidencia y Vicepresidencia',
    descripcion='Elección de Presidente y Vicepresidente',
    es_uninominal=True,  # Es uninominal
    permite_lista_cerrada=False,
    permite_lista_abierta=False,
    permite_coaliciones=False,
    activo=True,
    orden=1
)
```

### 4.2 Crear Candidatos

```python
# Para elección uninominal (Presidencia)
candidato_pres = Candidato(
    codigo='PRES-001',
    nombre_completo='Gustavo Petro Urrego',
    partido_id=1,  # Pacto Histórico
    tipo_eleccion_id=1,  # Presidencia
    numero_lista=None,  # No aplica en uninominales
    es_independiente=False,
    es_cabeza_lista=False,  # No aplica
    activo=True
)

# Para elección de corporación (Senado)
candidato_sen = Candidato(
    codigo='SEN-LIB-001',
    nombre_completo='Juan Manuel Galán',
    partido_id=2,  # Partido Liberal
    tipo_eleccion_id=2,  # Senado
    numero_lista=1,  # Posición en la lista
    es_independiente=False,
    es_cabeza_lista=True,  # Cabeza de lista
    activo=True
)
```

---

## 5. Registro de Votos por Testigos

### 5.1 Elección Uninominal (Presidencia)

**Pantalla del testigo**:
```
┌─────────────────────────────────────────┐
│ Formulario E-14 - Presidencia           │
├─────────────────────────────────────────┤
│                                         │
│ Candidatos:                             │
│                                         │
│ ○ Gustavo Petro - Francia Márquez      │
│   (Pacto Histórico)                     │
│   Votos: [____]                         │
│                                         │
│ ○ Rodolfo Hernández - Marelen Castillo │
│   (Liga de Gobernantes Anticorrupción)  │
│   Votos: [____]                         │
│                                         │
│ ○ Federico Gutiérrez - Rodrigo Lara    │
│   (Equipo por Colombia)                 │
│   Votos: [____]                         │
│                                         │
│ Votos Nulos: [____]                     │
│ Votos en Blanco: [____]                 │
│                                         │
│ [Guardar Formulario]                    │
└─────────────────────────────────────────┘
```

### 5.2 Elección de Corporación (Senado)

**Pantalla del testigo**:
```
┌─────────────────────────────────────────┐
│ Formulario E-14 - Senado                │
├─────────────────────────────────────────┤
│                                         │
│ Votos por Partido:                      │
│                                         │
│ [Logo] Partido Liberal                  │
│        Votos: [____]                    │
│                                         │
│ [Logo] Partido Conservador              │
│        Votos: [____]                    │
│                                         │
│ [Logo] Centro Democrático               │
│        Votos: [____]                    │
│                                         │
│ ─────────────────────────────────────   │
│                                         │
│ Votos Preferentes (Candidatos):         │
│                                         │
│ Partido Liberal:                        │
│   • Juan Manuel Galán: [____]           │
│   • María José Pizarro: [____]          │
│                                         │
│ Partido Conservador:                    │
│   • David Barguil: [____]               │
│   • Paola Holguín: [____]               │
│                                         │
│ Votos Nulos: [____]                     │
│ Votos en Blanco: [____]                 │
│                                         │
│ [Guardar Formulario]                    │
└─────────────────────────────────────────┘
```

---

## 6. Consolidación en E-24

### 6.1 Elección Uninominal

**E-24 solo muestra votos por candidato**:
```
┌─────────────────────────────────────────┐
│ E-24 - Presidencia                      │
│ Puesto: Centro - Medellín               │
├─────────────────────────────────────────┤
│                                         │
│ Candidato                    | Votos    │
│ ─────────────────────────────┼─────────│
│ Gustavo Petro                | 12,450   │
│ Rodolfo Hernández             | 10,230   │
│ Federico Gutiérrez            |  8,120   │
│ ─────────────────────────────┼─────────│
│ Votos Nulos                  |    450   │
│ Votos en Blanco              |    320   │
│ ─────────────────────────────┼─────────│
│ TOTAL                        | 31,570   │
└─────────────────────────────────────────┘
```

### 6.2 Elección de Corporación

**E-24 muestra votos por partido Y por candidato**:
```
┌─────────────────────────────────────────┐
│ E-24 - Senado                           │
│ Municipio: Medellín                     │
├─────────────────────────────────────────┤
│                                         │
│ VOTOS POR PARTIDO                       │
│ ─────────────────────────────┬─────────│
│ Partido                      | Votos    │
│ ─────────────────────────────┼─────────│
│ Partido Liberal              | 45,230   │
│ Partido Conservador          | 38,120   │
│ Centro Democrático           | 32,450   │
│ Pacto Histórico              | 28,900   │
│ ─────────────────────────────┼─────────│
│                                         │
│ VOTOS PREFERENTES (TOP 10)              │
│ ─────────────────────────────┬─────────│
│ Candidato (Partido)          | Votos    │
│ ─────────────────────────────┼─────────│
│ Juan M. Galán (Liberal)      | 12,450   │
│ David Barguil (Conservador)  | 10,230   │
│ María J. Pizarro (Liberal)   |  9,120   │
│ Paola Holguín (Conservador)  |  8,450   │
│ ...                          |   ...    │
│ ─────────────────────────────┼─────────│
│                                         │
│ Votos Nulos: 2,450                      │
│ Votos en Blanco: 1,320                  │
│ TOTAL: 148,470                          │
└─────────────────────────────────────────┘
```

---

## 7. Verificación por Tipo de Elección

### Consultas SQL

```sql
-- Verificar tipos de elección configurados
SELECT 
    codigo,
    nombre,
    es_uninominal,
    permite_lista_cerrada,
    permite_lista_abierta,
    permite_coaliciones,
    activo
FROM tipos_eleccion
ORDER BY orden;

-- Verificar candidatos por tipo
SELECT 
    te.nombre as tipo_eleccion,
    te.es_uninominal,
    COUNT(c.id) as total_candidatos,
    COUNT(DISTINCT c.partido_id) as total_partidos
FROM tipos_eleccion te
LEFT JOIN candidatos c ON c.tipo_eleccion_id = te.id AND c.activo = 1
WHERE te.activo = 1
GROUP BY te.id, te.nombre, te.es_uninominal;

-- Verificar votos registrados por tipo
SELECT 
    te.nombre as tipo_eleccion,
    te.es_uninominal,
    COUNT(DISTINCT f.id) as total_formularios,
    SUM(f.total_votos) as total_votos,
    COUNT(DISTINCT vp.id) as votos_partido_registrados,
    COUNT(DISTINCT vc.id) as votos_candidato_registrados
FROM tipos_eleccion te
LEFT JOIN formularios_e14 f ON f.tipo_eleccion_id = te.id
LEFT JOIN votos_partidos vp ON vp.formulario_id = f.id
LEFT JOIN votos_candidatos vc ON vc.formulario_id = f.id
WHERE te.activo = 1
GROUP BY te.id, te.nombre, te.es_uninominal;
```

---

## 8. Checklist de Configuración

### Para Elecciones Uninominales

- [ ] Crear tipo de elección con `es_uninominal = True`
- [ ] Crear candidatos (sin número de lista)
- [ ] NO crear votos por partido en E-14
- [ ] Solo registrar votos por candidato
- [ ] E-24 solo muestra candidatos

### Para Elecciones de Corporaciones

- [ ] Crear tipo de elección con `es_uninominal = False`
- [ ] Configurar si permite lista cerrada/abierta
- [ ] Crear candidatos con número de lista
- [ ] Marcar cabeza de lista
- [ ] Registrar votos por partido Y por candidato
- [ ] E-24 muestra partidos y candidatos
- [ ] Calcular cifra repartidora (opcional)

---

**Última actualización**: 30 de Noviembre de 2025  
**Versión**: 1.0
