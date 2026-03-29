import django_filters
from .models import Producto, Proveedor, MovimientoInventario, Categoria


class ProductoFilter(django_filters.FilterSet):
    """Filtros para Producto"""
    nombre = django_filters.CharFilter(
        field_name='nombre',
        lookup_expr='icontains',
        label='Buscar por nombre'
    )
    precio_min = django_filters.NumberFilter(
        field_name='precio',
        lookup_expr='gte',
        label='Precio mínimo'
    )
    precio_max = django_filters.NumberFilter(
        field_name='precio',
        lookup_expr='lte',
        label='Precio máximo'
    )
    categoria = django_filters.ModelChoiceFilter(
        queryset=Categoria.objects.all(),
        label='Categoría'
    )
    disponible = django_filters.BooleanFilter(label='Disponible')

    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'disponible', 'precio_min', 'precio_max']


class ProveedorFilter(django_filters.FilterSet):
    """Filtros para Proveedor"""
    nombre = django_filters.CharFilter(
        field_name='nombre',
        lookup_expr='icontains',
        label='Buscar por nombre'
    )
    email = django_filters.CharFilter(
        field_name='email',
        lookup_expr='icontains',
        label='Buscar por email'
    )
    ciudad = django_filters.CharFilter(
        field_name='ciudad',
        lookup_expr='icontains',
        label='Buscar por ciudad'
    )

    class Meta:
        model = Proveedor
        fields = ['nombre', 'email', 'ciudad']


class MovimientoInventarioFilter(django_filters.FilterSet):
    """Filtros para MovimientoInventario"""
    tipo = django_filters.ChoiceFilter(
        choices=[('entrada', 'Entrada'), ('salida', 'Salida')],
        label='Tipo de movimiento'
    )
    producto = django_filters.ModelChoiceFilter(
        queryset=Producto.objects.all(),
        label='Producto'
    )
    proveedor = django_filters.ModelChoiceFilter(
        queryset=Proveedor.objects.all(),
        label='Proveedor'
    )
    fecha = django_filters.DateFromToRangeFilter(
        field_name='fecha',
        label='Rango de fecha'
    )

    class Meta:
        model = MovimientoInventario
        fields = ['tipo', 'producto', 'proveedor', 'fecha']
