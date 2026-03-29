from django.urls import path, include

from . import views

# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register(r'categorias', views.CategoriaViewSet)

urlpatterns = [
    # path('contact/<str:name>', views.contact),
    # path('categorias', views.categorias, name="categorias"),
    # path('productos', views.productoFormView),
    # path(
    #     'clase8',  views.index
    # )
    # path('', include(router.urls)),
    # path('categoria', views.CategoriaViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('categoria/<int:pk>', views.CategoriaViewSet.as_view({'get': 'retrieve'})),
    path('api/categorias/', views.CategoriaCreateView.as_view(), name='api-categorias'),
    path('api/productos/', views.ProductoListCreateView.as_view(), name='api-productos'),
    path('api/proveedores/', views.ProveedorListCreateView.as_view(), name='api-proveedores'),
    path('api/movimientos/', views.MovimientoInventarioListCreateView.as_view(), name='api-movimientos'),
    path('categorias/cantidad', views.categoria_count),
    path('productos/filtrar/unidades', views.producto_en_unidades),
    path('reporte/productos', views.reporte_productos),
    # path('enviar/mensaje', views.enviar_mensaje),
]

