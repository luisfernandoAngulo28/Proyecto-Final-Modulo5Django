from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .forms import ProductoForm

from .models import Categoria, Producto, Proveedor, MovimientoInventario
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics, filters
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    CategoriaSerializer,
    ProductoSerializer,
    ProveedorSerializer,
    MovimientoInventarioSerializer,
    ReporteProductoSerializer,
    ContactSerializer,
)
from .filters import ProductoFilter, ProveedorFilter, MovimientoInventarioFilter

from rest_framework.permissions import IsAuthenticated

from .permissions import IsUserAlmacen

from .utils import permission_required

import logging

logger = logging.getLogger(__name__)

def index(request):
    return HttpResponse("Hola mundo")

def contact(request, name):
    return HttpResponse(f"Hola {name} bienvenido a la clase de Django")

def categorias(request):
    post_nombre = request.POST.get('nombre')
    if post_nombre:
        q = Categoria(nombre=post_nombre)
        q.save()

    filtro_nombre = request.GET.get('nombre')
    if filtro_nombre:
        categorias = Categoria.objects.filter(nombre__contains=filtro_nombre)
    else:
        categorias = Categoria.objects.all()
    return render(request, 'form_categorias.html', {
        "categorias": categorias
    })

def productoFormView(request):
    form = ProductoForm()
    producto = None
    id_producto = request.GET.get('id')
    if id_producto:
        producto = get_object_or_404(Producto, id=id_producto)
        form = ProductoForm(instance=producto)

    if request.method == 'POST':
        if producto:
            form = ProductoForm(request.POST, instance=producto)
        else:
            form = ProductoForm(request.POST)

    if form.is_valid():
        form.save()

    return render(request, 'form_productos.html', {
        "form":form
    })


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]


class CategoriaCreateView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre', 'id']
    ordering = ['nombre']


class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all().select_related('categoria')
    serializer_class = ProductoSerializer
    filterset_class = ProductoFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'precio', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        POST requiere autenticación, GET es público
        """
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []


class ProveedorListCreateView(generics.ListCreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    filterset_class = ProveedorFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'email', 'ciudad']
    ordering_fields = ['nombre', 'email']
    ordering = ['nombre']

    def get_permissions(self):
        """
        POST requiere autenticación, GET es público
        """
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []


class MovimientoInventarioListCreateView(generics.ListCreateAPIView):
    queryset = MovimientoInventario.objects.all().select_related('producto', 'proveedor')
    serializer_class = MovimientoInventarioSerializer
    filterset_class = MovimientoInventarioFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['fecha', 'cantidad', 'tipo']
    ordering = ['-fecha']
    permission_classes = [IsAuthenticated]  # Require auth para todos los métodos

@api_view(['GET'])
def categoria_count(request):
    try:
        cantidad = Categoria.objects.count()
        return JsonResponse({"cantidad": cantidad}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
def producto_en_unidades(request):
    try:
        productos = Producto.objects.filter(unidades="u")
        return JsonResponse(ProductoSerializer(productos, many=True).data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
@permission_required(["inventario.reporte_cantidad"])
# @permission_classes([IsUserAlmacen])
def reporte_productos(request):
    try:
        cantidad = Producto.objects.count()
        productos = Producto.objects.filter(unidades="u")
        logger.info(f"Reporte de productos {cantidad}")
        return JsonResponse(ReporteProductoSerializer({
            "cantidad": cantidad,
            "productos": productos
        }).data, safe=False, status=200)
    except Exception as e:
        logger.error("Se produjo un error")
        return JsonResponse({"message": str(e)}, status=400)

@api_view(['POST'])
def enviar_mensaje(request):
    cs = ContactSerializer(data=request.data)
    if cs.is_valid():
        return JsonResponse({"message": "Mensaje enviado"}, status=200)
    else:
        return JsonResponse({"message": cs.errors}, status=400)

