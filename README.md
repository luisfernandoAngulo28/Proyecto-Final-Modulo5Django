# Ecoapp - Proyecto Django Módulo V

Sistema de gestión de inventario desarrollado en Django con Django REST Framework.

## Descripción

Este proyecto implementa una API REST completa para la gestión de inventario, categorías de productos, proveedores y movimientos de inventario. Incluye validaciones personalizadas, autenticación JWT, y un panel de administración Django completamente configurado.

## Requisitos del Sistema

- Python 3.11+
- PostgreSQL 12+ (opcional, también funciona con SQLite)
- pip o conda

## Instalación

### 1. Clonar el repositorio

```sh
git clone https://github.com/luisfernandoAngulo28/Proyecto-Final-Modulo5Django.git
cd Proyecto-Final-Modulo5Django
```

### 2. Crear entorno virtual

```sh
python -m venv .venv
```

**Activar entorno:**
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

### 3. Instalar dependencias

```sh
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env` con tus credenciales (ya incluido en el proyecto):

```env
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
SECRET_KEY=change-secret-key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=BDEco_App
DB_USER=postgres
DB_PASSWORD=12345678
DB_HOST=localhost
DB_PORT=5432
TIME_ZONE=America/La_Paz
LANGUAGE_CODE=en-EN
```

### 5. Ejecutar migraciones

```sh
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear SuperAdministrador

```sh
python manage.py createsuperuser
```

Credenciales de prueba:
- Usuario: `admin`
- Contraseña: `admin123`

### 7. Cargar datos iniciales (opcional)

```sh
python manage.py loaddata dump_inventario.json
```

### 8. Ejecutar servidor de desarrollo

```sh
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

## Documentación de API

### Autenticación

La mayoría de endpoints requieren token JWT. Obtén el token en:

```
POST /api/token/
```

Con credenciales:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

Respuesta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Incluye en headers: `Authorization: Bearer <access_token>`

### Endpoints disponibles

#### Categorías
- `GET /inventario/api/categorias/` - Listar categorías
- `POST /inventario/api/categorias/` - Crear categoría
- `GET /inventario/categorias/cantidad` - Cantidad total de categorías (Custom API)

#### Productos
- `GET /inventario/api/productos/` - Listar productos
- `POST /inventario/api/productos/` - Crear producto
- `GET /inventario/productos/filtrar/unidades` - Filtrar por unidades (Custom API)

#### Proveedores
- `GET /inventario/api/proveedores/` - Listar proveedores
- `POST /inventario/api/proveedores/` - Crear proveedor

#### Movimientos de Inventario
- `GET /inventario/api/movimientos/` - Listar movimientos
- `POST /inventario/api/movimientos/` - Crear movimiento

#### Reportes (Custom APIs)
- `GET /inventario/reporte/productos` - Reporte de productos disponibles
- `POST /inventario/enviar/mensaje` - Enviar mensajes

#### Documentación Interactiva
- `GET /swagger/` - Documentación Swagger UI
- `GET /redoc/` - Documentación ReDoc
- `GET /admin/` - Panel de administración Django

## Modelos de Datos

### Categoria
- `nombre` (CharField): Nombre de la categoría (sin números)
- Permisos personalizados: reporte_cantidad, reporte_detalle

### Producto
- `nombre` (CharField): Nombre único (sin números)
- `categoria` (ForeignKey): Referencia a Categoria
- `descripcion` (TextField): Descripción detallada
- `precio` (DecimalField): Precio (debe ser par)
- `unidades` (CharField): Unidades o Kilogramos
- `disponible` (BooleanField): Estado disponibilidad
- `created_at` (DateTimeField): Fecha de creación
- `updated_at` (DateTimeField): Última actualización

### Proveedor
- `nombre` (CharField): Nombre proveedor (sin números)
- `email` (EmailField): Email único
- `telefono` (CharField): Teléfono opcional
- `ciudad` (CharField): Ciudad opcional

### MovimientoInventario
- `producto` (ForeignKey): Referencia a Producto
- `proveedor` (ForeignKey): Referencia a Proveedor
- `tipo` (CharField): entrada/salida
- `cantidad` (PositiveIntegerField): Cantidad movida
- `observacion` (TextField): Notas opcionales
- `fecha` (DateTimeField): Fecha de movimiento

## Validaciones Personalizadas

1. **validar_par**: Valida que precios sean números pares
2. **validar_texto_sin_numeros**: Valida que nombres no contengan dígitos

## Pruebas

Ejecutar suite de tests:

```sh
python manage.py test
```

Pruebas incluidas:
- Modelos y validadores
- Serializers
- Vistas y endpoints

## Panel de Administración

Accede en `http://127.0.0.1:8000/admin/`

Modelos registrados:
- Categorías (con búsqueda y filtros)
- Productos (con ordenamiento y búsqueda)
- Proveedores (con búsqueda y filtros)
- Movimientos de Inventario (con filtros por tipo y fecha)

## Estructura del Proyecto

```
.
├── ecoapp/              # Configuración principal
│   ├── settings.py      # Configuración con variables de entorno
│   ├── urls.py          # URLs principales
│   └── wsgi.py
├── inventario/          # Aplicación principal
│   ├── models.py        # 4 modelos: Categoria, Producto, Proveedor, MovimientoInventario
│   ├── views.py         # 3+ GenericAPIView + Custom APIs
│   ├── serializers.py   # Serializers con validaciones
│   ├── urls.py          # URLs de inventario
│   ├── validators.py    # Validadores personalizados
│   ├── admin.py         # Configuración admin
│   ├── forms.py         # Formularios Django
│   └── migrations/      # Migraciones de BD
├── .env                 # Variables de entorno
├── requirements.txt     # Dependencias
├── manage.py
├── TAREA_MODULO_V.md    # Enunciado de la tarea
├── INTEGRANTES.md       # Información de integrantes
└── README.md            # Este archivo
```

## Contribuciones

Estudiante: Luis Fernando Angulo Heredia
Docente: Juan Marcelo Arteaga Gutierrez

## Licencia

MIT License
# Proyecto-Final-Modulo5Django
