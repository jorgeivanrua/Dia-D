# Estructura de Ubicaciones para Usuarios

## 📍 Jerarquía de Ubicaciones DIVIPOLA

```
Departamento (44)
  └── Municipio (4401)
      └── Zona (440101)
          └── Puesto (44010101)
              └── Mesa (4401010101)
```

## 👥 Ubicación por Rol de Usuario

### **Super Admin**
- **Ubicación:** `NULL` (sin ubicación)
- **Acceso:** Global a todo el sistema
- **Ejemplo:** `admin` (sin ubicación específica)

### **Admin Departamental**
- **Ubicación:** Departamento
- **Acceso:** Todo el departamento
- **Ejemplo:** `admin_caqueta` → Ubicación: Caquetá (44)
- **Puede ver:** Todos los municipios, zonas, puestos y mesas del departamento

### **Admin Municipal**
- **Ubicación:** Municipio
- **Acceso:** Todo el municipio
- **Ejemplo:** `admin_florencia` → Ubicación: Florencia (4401)
- **Puede ver:** Todas las zonas, puestos y mesas del municipio

### **Coordinador Departamental**
- **Ubicación:** Departamento
- **Acceso:** Todo el departamento
- **Ejemplo:** `coord_dpto_caqueta` → Ubicación: Caquetá (44)
- **Puede ver:** Todos los municipios, zonas, puestos y mesas del departamento

### **Coordinador Municipal**
- **Ubicación:** Municipio
- **Acceso:** Todo el municipio
- **Ejemplo:** `coord_mun_florencia` → Ubicación: Florencia (4401)
- **Puede ver:** Todas las zonas, puestos y mesas del municipio

### **Coordinador de Puesto**
- **Ubicación:** Puesto (incluye departamento, municipio, zona, puesto)
- **Acceso:** Solo su puesto y sus mesas
- **Ejemplo:** `coord_puesto_44010101` → Ubicación: Puesto específico
- **Puede ver:** Solo las mesas de su puesto
- **Estructura de ubicación:**
  ```
  {
    departamento_codigo: "44",
    municipio_codigo: "4401",
    zona_codigo: "440101",
    puesto_codigo: "44010101",
    tipo: "puesto"
  }
  ```

### **Testigo Electoral**
- **Ubicación:** Puesto (incluye departamento, municipio, zona, puesto)
- **Acceso:** Solo su puesto y sus mesas
- **Ejemplo:** `testigo_44010101_1` → Ubicación: Puesto específico
- **Puede reportar:** Desde cualquier mesa de su puesto
- **Estructura de ubicación:**
  ```
  {
    departamento_codigo: "44",
    municipio_codigo: "4401",
    zona_codigo: "440101",
    puesto_codigo: "44010101",
    tipo: "puesto"
  }
  ```

### **Auditor Electoral**
- **Ubicación:** Departamento
- **Acceso:** Todo el departamento (solo lectura)
- **Ejemplo:** `auditor_caqueta` → Ubicación: Caquetá (44)
- **Puede ver:** Todos los datos del departamento sin modificar

## 🔑 Login por Ubicación

### Ejemplo de Login para Testigo:

```json
{
  "rol": "testigo_electoral",
  "departamento_codigo": "44",
  "municipio_codigo": "4401",
  "zona_codigo": "440101",
  "puesto_codigo": "44010101",
  "password": "test123"
}
```

El sistema:
1. Busca la ubicación de tipo "puesto" con esos códigos
2. Busca un usuario con rol "testigo_electoral" y esa ubicación
3. Verifica la contraseña
4. Genera el token JWT

## 📊 Tabla de Ubicaciones

| Rol | Tipo de Ubicación | Códigos Necesarios | Ejemplo |
|-----|-------------------|-------------------|---------|
| Super Admin | NULL | Ninguno | - |
| Admin Departamental | departamento | departamento_codigo | 44 |
| Admin Municipal | municipio | departamento_codigo, municipio_codigo | 44, 4401 |
| Coordinador Departamental | departamento | departamento_codigo | 44 |
| Coordinador Municipal | municipio | departamento_codigo, municipio_codigo | 44, 4401 |
| Coordinador Puesto | puesto | departamento, municipio, zona, puesto | 44, 4401, 440101, 44010101 |
| Testigo Electoral | puesto | departamento, municipio, zona, puesto | 44, 4401, 440101, 44010101 |
| Auditor | departamento | departamento_codigo | 44 |

## ⚠️ Notas Importantes

1. **Testigos y Coordinadores de Puesto** tienen la misma estructura de ubicación (puesto)
2. La ubicación de tipo "puesto" incluye automáticamente toda la jerarquía (depto, muni, zona, puesto)
3. Los testigos NO se asignan a mesas específicas, sino a puestos
4. Un testigo puede reportar desde cualquier mesa de su puesto
5. La mesa específica se selecciona al crear el formulario E-14

## 🔄 Flujo de Creación de Usuarios

### Testigo Electoral:

```python
# 1. Obtener el puesto
puesto = Location.query.filter_by(
    tipo='puesto',
    departamento_codigo='44',
    municipio_codigo='4401',
    zona_codigo='440101',
    puesto_codigo='44010101'
).first()

# 2. Crear el testigo
testigo = User(
    nombre='testigo_44010101_1',
    rol='testigo_electoral',
    ubicacion_id=puesto.id,  # ← Ubicación = PUESTO
    activo=True
)
testigo.set_password('test123')
```

### Coordinador de Puesto:

```python
# 1. Obtener el puesto
puesto = Location.query.filter_by(
    tipo='puesto',
    departamento_codigo='44',
    municipio_codigo='4401',
    zona_codigo='440101',
    puesto_codigo='44010101'
).first()

# 2. Crear el coordinador
coordinador = User(
    nombre='coord_puesto_44010101',
    rol='coordinador_puesto',
    ubicacion_id=puesto.id,  # ← Ubicación = PUESTO
    activo=True
)
coordinador.set_password('test123')
```

## ✅ Validación en Login

El sistema valida que:
1. El rol corresponda al tipo de ubicación correcto
2. La ubicación exista en la base de datos
3. Haya un usuario con ese rol y ubicación
4. La contraseña sea correcta

---

**Última actualización:** 2025-11-27  
**Versión:** 1.0
