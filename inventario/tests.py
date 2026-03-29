from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Categoria, Producto, Proveedor, MovimientoInventario, ProductUnits
from .validators import validar_par, validar_texto_sin_numeros


# ============== PRUEBAS DE VALIDADORES ==============
class ValidadoresTestCase(TestCase):
    """Tests para validadores personalizados"""

    def test_validar_par_valido(self):
        """Debe aceptar números pares"""
        try:
            validar_par(2)
            validar_par(100)
        except ValidationError:
            self.fail("validar_par lanzó ValidationError para número par")

    def test_validar_par_invalido(self):
        """Debe rechazar números impares"""
        with self.assertRaises(ValidationError):
            validar_par(3)
        with self.assertRaises(ValidationError):
            validar_par(99)

    def test_validar_texto_sin_numeros_valido(self):
        """Debe aceptar texto sin números"""
        try:
            validar_texto_sin_numeros("Electrónica")
            validar_texto_sin_numeros("Bebidas")
        except ValidationError:
            self.fail("validar_texto_sin_numeros rechazó texto válido")

    def test_validar_texto_sin_numeros_invalido(self):
        """Debe rechazar texto con números"""
        with self.assertRaises(ValidationError):
            validar_texto_sin_numeros("Categoría123")
        with self.assertRaises(ValidationError):
            validar_texto_sin_numeros("Producto2024")


# ============== PRUEBAS DE MODELOS ==============
class CategoriaModelTestCase(TestCase):
    """Tests para modelo Categoria"""

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Electrónica")

    def test_crear_categoria(self):
        """Debe crear una categoría correctamente"""
        self.assertEqual(Categoria.objects.count(), 1)
        self.assertEqual(self.categoria.nombre, "Electrónica")

    def test_str_categoria(self):
        """El __str__ debe retornar el nombre"""
        self.assertEqual(str(self.categoria), "Electrónica")

    def test_categoria_nombre_sin_numeros(self):
        """No debe permitir números en nombres de categorías"""
        with self.assertRaises(ValidationError):
            categoría_invalida = Categoria(nombre="Electrónica123")
            categoría_invalida.full_clean()


class ProductoModelTestCase(TestCase):
    """Tests para modelo Producto"""

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Electrónica")
        self.producto = Producto.objects.create(
            nombre="Laptop",
            categoria=self.categoria,
            descripcion="Laptop de 15 pulgadas",
            precio=4000,
            unidades=ProductUnits.UNITS
        )

    def test_crear_producto(self):
        """Debe crear un producto correctamente"""
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(self.producto.nombre, "Laptop")

    def test_producto_precio_par(self):
        """El precio debe ser un número par"""
        # La creación fue exitosa porque 4000 es par
        self.assertEqual(self.producto.precio, 4000)

    def test_producto_precio_impar(self):
        """No debe permitir precios impares"""
        with self.assertRaises(ValidationError):
            producto_invalido = Producto(
                nombre="Mouse",
                categoria=self.categoria,
                descripcion="Mouse inalámbrico",
                precio=99,  # número impar
                unidades=ProductUnits.UNITS
            )
            producto_invalido.full_clean()

    def test_producto_nombre_unico(self):
        """El nombre debe ser único"""
        with self.assertRaises(Exception):
            Producto.objects.create(
                nombre="Laptop",
                categoria=self.categoria,
                descripcion="Otra laptop",
                precio=3000,
                unidades=ProductUnits.UNITS
            )

    def test_str_producto(self):
        """El __str__ debe retornar el nombre"""
        self.assertEqual(str(self.producto), "Laptop")


class ProveedorModelTestCase(TestCase):
    """Tests para modelo Proveedor"""

    def setUp(self):
        self.proveedor = Proveedor.objects.create(
            nombre="Distribuidor XYZ",
            email="contacto@xyz.com",
            telefono="555-1234",
            ciudad="La Paz"
        )

    def test_crear_proveedor(self):
        """Debe crear un proveedor correctamente"""
        self.assertEqual(Proveedor.objects.count(), 1)
        self.assertEqual(self.proveedor.nombre, "Distribuidor XYZ")

    def test_proveedor_email_unico(self):
        """El email debe ser único"""
        with self.assertRaises(Exception):
            Proveedor.objects.create(
                nombre="Otro Distribuidor",
                email="contacto@xyz.com",
                telefono="555-5678",
                ciudad="Cochabamba"
            )

    def test_str_proveedor(self):
        """El __str__ debe retornar el nombre"""
        self.assertEqual(str(self.proveedor), "Distribuidor XYZ")


class MovimientoInventarioModelTestCase(TestCase):
    """Tests para modelo MovimientoInventario"""

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Electrónica")
        self.producto = Producto.objects.create(
            nombre="Teclado",
            categoria=self.categoria,
            descripcion="Teclado mecánico",
            precio=200,
            unidades=ProductUnits.UNITS
        )
        self.proveedor = Proveedor.objects.create(
            nombre="Tech Distribuidor",
            email="tech@distribuidor.com"
        )
        self.movimiento = MovimientoInventario.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            tipo="entrada",
            cantidad=50
        )

    def test_crear_movimiento(self):
        """Debe crear un movimiento correctamente"""
        self.assertEqual(MovimientoInventario.objects.count(), 1)
        self.assertEqual(self.movimiento.cantidad, 50)

    def test_str_movimiento(self):
        """El __str__ debe retornar descripción formateada"""
        self.assertEqual(str(self.movimiento), "entrada - Teclado (50)")


# ============== PRUEBAS DE API (ENDPOINTS) ==============
class CategoriaAPITestCase(APITestCase):
    """Tests para endpoints de Categoría"""

    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(nombre="Hogar")

    def test_listar_categorias(self):
        """GET /inventario/api/categorias/ debe retornar lista"""
        response = self.client.get('/inventario/api/categorias/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_categoria(self):
        """POST /inventario/api/categorias/ debe crear categoría"""
        data = {"nombre": "Deportes"}
        response = self.client.post('/inventario/api/categorias/', data, content_type='application/json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

    def test_categoria_cantidad_custom_api(self):
        """GET /inventario/categorias/cantidad debe retornar cantidad"""
        response = self.client.get('/inventario/categorias/cantidad')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('cantidad', response.json())


class ProductoAPITestCase(APITestCase):
    """Tests para endpoints de Producto"""

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Muebles")
        self.producto = Producto.objects.create(
            nombre="Silla",
            categoria=self.categoria,
            descripcion="Silla de oficina",
            precio=150,
            unidades=ProductUnits.UNITS
        )

    def test_listar_productos(self):
        """GET /inventario/api/productos/ debe retornar lista"""
        response = self.client.get('/inventario/api/productos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_producto(self):
        """POST /inventario/api/productos/ debe crear producto"""
        data = {
            "nombre": "Mesa",
            "categoria": self.categoria.id,
            "descripcion": "Mesa de 6 puestos",
            "precio": 400,
            "unidades": "u"
        }
        response = self.client.post('/inventario/api/productos/', data, content_type='application/json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])


class ProveedorAPITestCase(APITestCase):
    """Tests para endpoints de Proveedor"""

    def setUp(self):
        self.proveedor = Proveedor.objects.create(
            nombre="Proveedor Local",
            email="local@proveedor.com"
        )

    def test_listar_proveedores(self):
        """GET /inventario/api/proveedores/ debe retornar lista"""
        response = self.client.get('/inventario/api/proveedores/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_proveedor(self):
        """POST /inventario/api/proveedores/ debe crear proveedor"""
        data = {
            "nombre": "Nuevo Proveedor",
            "email": "nuevo@proveedor.com",
            "telefono": "555-9999"
        }
        response = self.client.post('/inventario/api/proveedores/', data, content_type='application/json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])


class MovimientoAPITestCase(APITestCase):
    """Tests para endpoints de MovimientoInventario"""

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Papelería")
        self.producto = Producto.objects.create(
            nombre="Papel",
            categoria=self.categoria,
            descripcion="Papel blanco A4",
            precio=100,
            unidades=ProductUnits.UNITS
        )
        self.proveedor = Proveedor.objects.create(
            nombre="Papelera Central",
            email="papelera@central.com"
        )

    def test_listar_movimientos(self):
        """GET /inventario/api/movimientos/ debe retornar lista"""
        response = self.client.get('/inventario/api/movimientos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_movimiento(self):
        """POST /inventario/api/movimientos/ debe crear movimiento"""
        data = {
            "producto": self.producto.id,
            "proveedor": self.proveedor.id,
            "tipo": "entrada",
            "cantidad": 100
        }
        response = self.client.post('/inventario/api/movimientos/', data, content_type='application/json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
