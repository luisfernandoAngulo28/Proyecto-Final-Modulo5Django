# Guía de Pruebas con Postman - Proyecto EcoApp

## Configuración Inicial

### 1. Crear una variable de entorno en Postman

En Postman:
- **Manage Environments** → **Create** una nueva llamada "EcoApp Dev"
- Agrega estas variables:

| Variable | Valor |
|----------|-------|
| `base_url` | `http://127.0.0.1:8000` |
| `token` | (se llenará automáticamente) |
| `user` | `admin` |
| `password` | `admin123` |

---

## 1️⃣ Obtener Token JWT (Autenticación)

**Método:** POST  
**URL:** `{{base_url}}/api/token/`  
**Body (JSON):**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Test Script (automatizar token):**
```javascript
if (pm.response.code === 200) {
    pm.environment.set("token", pm.response.json().access);
}
```

**Headers:**
```
Content-Type: application/json
```

---

## 2️⃣ CATEGORÍAS

### Listar Categorías
- **GET** `{{base_url}}/inventario/api/categorias/`
- Headers: (ninguno necesario para GET)
- Parámetros opcionales: `?ordering=-nombre&search=Electro`

### Obtener Cantidad de Categorías (Custom API)
- **GET** `{{base_url}}/inventario/categorias/cantidad`

### Crear Categoría
- **POST** `{{base_url}}/inventario/api/categorias/`
- Headers: `Authorization: Bearer {{token}}`
- Body:
```json
{
  "nombre": "Nuevos Productos"
}
```

---

## 3️⃣ PRODUCTOS

### Listar Productos (con filtrado avanzado)
- **GET** `{{base_url}}/inventario/api/productos/`
- Ejemplos de filtrado:
  - `?nombre=laptop` - buscar por nombre
  - `?precio_min=100&precio_max=500` - rango de precio
  - `?categoria=1` - por categoría
  - `?disponible=true` - solo disponibles
  - `?ordering=-precio` - ordenar por precio descendente
  - `?page=2` - paginación (10 items por página)

### Filtrar por Unidades (Custom API)
- **GET** `{{base_url}}/inventario/productos/filtrar/unidades`

### Crear Producto
- **POST** `{{base_url}}/inventario/api/productos/`
- Headers: `Authorization: Bearer {{token}}`
- Body:
```json
{
  "nombre": "Monitor LG 24 pulgadas",
  "categoria": 1,
  "descripcion": "Monitor Full HD IPS",
  "precio": 300,
  "unidades": "u",
  "disponible": true
}
```

**Nota:** El precio debe ser PAR (número divisible por 2)

---

## 4️⃣ PROVEEDORES

### Listar Proveedores (con filtrado)
- **GET** `{{base_url}}/inventario/api/proveedores/`
- Filtrado: `?nombre=distribuidor&ciudad=La Paz`

### Crear Proveedor
- **POST** `{{base_url}}/inventario/api/proveedores/`
- Headers: `Authorization: Bearer {{token}}`
- Body:
```json
{
  "nombre": "TechDistribuidor Bolivia",
  "email": "contacto@techdist.bo",
  "telefono": "555-1234",
  "ciudad": "La Paz"
}
```

---

## 5️⃣ MOVIMIENTOS DE INVENTARIO

### Listar Movimientos (requiere autenticación)
- **GET** `{{base_url}}/inventario/api/movimientos/`
- Headers: `Authorization: Bearer {{token}}`
- Filtrado: `?tipo=entrada&ordering=-fecha`

### Crear Movimiento de Entrada
- **POST** `{{base_url}}/inventario/api/movimientos/`
- Headers: `Authorization: Bearer {{token}}`
- Body:
```json
{
  "producto": 1,
  "proveedor": 1,
  "tipo": "entrada",
  "cantidad": 50,
  "observacion": "Compra a proveedor autorizado"
}
```

### Crear Movimiento de Salida
```json
{
  "producto": 1,
  "proveedor": null,
  "tipo": "salida",
  "cantidad": 5,
  "observacion": "Venta a cliente"
}
```

---

## 6️⃣ DOCUMENTACIÓN INTERACTIVA

### Swagger UI (explorador visual)
- **GET** `{{base_url}}/swagger/`
- Accede desde el navegador para documentación interactiva

### ReDoc (documentación alternativa)
- **GET** `{{base_url}}/redoc/`

### Panel de Administración
- **GET** `{{base_url}}/admin/`
- Login: `admin` / `admin123`

---

## 7️⃣ REPORTES

### Reporte de Productos
- **GET** `{{base_url}}/inventario/reporte/productos`
- Headers: `Authorization: Bearer {{token}}`

### Respuesta esperada:
```json
{
  "cantidad": 15,
  "productos": [
    {
      "id": 1,
      "nombre": "Laptop",
      "precio": 4000,
      ...
    }
  ]
}
```

---

## 🔒 LIMITACIONES (Rate Limiting)

✅ **Usuarios Anónimos:** 100 requests/hora  
✅ **Usuarios Autenticados:** 1000 requests/hora  

Si excedes, recibirás: `429 Too Many Requests`

---

## 🧪 Casos de Prueba Recomendados

### ✅ Test Suite Básica
1. Login → Obtener token
2. Listar categorías
3. Crear categoría
4. Listar productos con filtros
5. Crear producto con precio válido
6. Intentar crear producto con precio impar (debe fallar)
7. Crear proveedor
8. Crear movimiento de entrada
9. Consultar reporte

### ❌ Test Suite de Errores (validar")
1. Crear producto SIN token (debe fallar)
2. Crear categoría con nombre con números (debe fallar)
3. Crear producto con precio impar (debe fallar)
4. Crear proveedor con email duplicado (debe fallar)
5. Paginar fuera de rango (`?page=999`)

---

## 📊 Ejemplo de Flujo Completo

```
1. POST /api/token/ → Obtener token
   ↓
2. POST /inventario/api/categorias/ → Crear categoría
   ↓
3. POST /inventario/api/productos/ → Crear producto en esa categoría
   ↓
4. POST /inventario/api/proveedores/ → Crear proveedor
   ↓
5. POST /inventario/api/movimientos/ → Registrar entrada de producto
   ↓
6. GET /inventario/reporte/productos → Ver reporte final
```

---

## Exportar Colección

Una vez importada en Postman, puedes:
- Guardar colección
- Exportar como JSON
- Compartir con compañeros

**Comando para testear todo:**
- En Postman → **Runner** → Selecciona la colección → Run
