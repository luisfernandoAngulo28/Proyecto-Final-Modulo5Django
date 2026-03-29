from django.db import models
from .validators import validar_par, validar_texto_sin_numeros


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, validators=[validar_texto_sin_numeros])

    def __str__(self):
        return self.nombre

    class Meta:
        permissions = [
            ("reporte_cantidad", "Visualizar el reporte de cantidad"),
            ("reporte_detalle", "Reporte detallado de cantidades"),
        ]


class ProductUnits(models.TextChoices):
    UNITS = 'u', 'Unidades'
    KG = 'kg', 'Kilogramos'

class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True, validators=[validar_texto_sin_numeros])
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2,
                                 validators=[validar_par])
    unidades = models.CharField(max_length=2, choices=ProductUnits.choices,
                                default=ProductUnits.UNITS)
    disponible = models.BooleanField(blank=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=120, validators=[validar_texto_sin_numeros])
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre


class TipoMovimiento(models.TextChoices):
    ENTRADA = 'entrada', 'Entrada'
    SALIDA = 'salida', 'Salida'


class MovimientoInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, null=True, blank=True, on_delete=models.SET_NULL)
    tipo = models.CharField(max_length=10, choices=TipoMovimiento.choices)
    cantidad = models.PositiveIntegerField()
    observacion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"
