from django.contrib import admin

from .models import Categoria, Producto, Proveedor, MovimientoInventario

admin.site.register(Categoria)


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'unidades', 'precio')
    ordering = ('precio',)
    search_fields = ('nombre',)
    list_filter = ('unidades',)

admin.site.register(Producto, ProductoAdmin)


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'ciudad')
    search_fields = ('nombre', 'email', 'ciudad')


class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'producto', 'proveedor', 'cantidad', 'fecha')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre', 'proveedor__nombre')


admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(MovimientoInventario, MovimientoInventarioAdmin)
