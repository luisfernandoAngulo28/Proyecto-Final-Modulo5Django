from rest_framework import serializers
from .models import Categoria, Producto, Proveedor, MovimientoInventario
from .validators import validar_subject


class CategoriaSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(
        max_length=100,
        required=True,
        error_messages={
            'required': 'El nombre de la categoría es requerido.',
            'blank': 'El nombre no puede estar vacío.',
            'max_length': 'El nombre no puede exceder 100 caracteres.'
        }
    )

    class Meta:
        model = Categoria
        fields = '__all__'

    def validate_nombre(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "El nombre de la categoría no debe contener números."
            )
        return value


class ProductoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'El nombre del producto es requerido.'}
    )
    precio = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        error_messages={
            'required': 'El precio es requerido.',
            'invalid': 'El precio debe ser un número válido.'
        }
    )

    class Meta:
        model = Producto
        fields = '__all__'

    def validate_nombre(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "El nombre del producto no debe contener números."
            )
        return value

    def validate_precio(self, value):
        if value % 2 != 0:
            raise serializers.ValidationError(
                "El precio debe ser un número par."
            )
        if value <= 0:
            raise serializers.ValidationError(
                "El precio debe ser mayor a cero."
            )
        return value


class ProveedorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'El email es requerido.',
            'invalid': 'Ingrese un email válido.'
        }
    )
    nombre = serializers.CharField(
        max_length=120,
        required=True,
        error_messages={'required': 'El nombre del proveedor es requerido.'}
    )

    class Meta:
        model = Proveedor
        fields = '__all__'

    def validate_nombre(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "El nombre no debe contener números."
            )
        return value


class MovimientoInventarioSerializer(serializers.ModelSerializer):
    tipo = serializers.ChoiceField(
        choices=['entrada', 'salida'],
        error_messages={
            'required': 'El tipo de movimiento es requerido.',
            'invalid_choice': 'Los tipos válidos son: entrada o salida.'
        }
    )
    cantidad = serializers.IntegerField(
        min_value=1,
        error_messages={
            'required': 'La cantidad es requerida.',
            'min_value': 'La cantidad debe ser mayor a cero.'
        }
    )

    class Meta:
        model = MovimientoInventario
        fields = '__all__'

    def validate(self, data):
        if data['cantidad'] <= 0:
            raise serializers.ValidationError(
                {"cantidad": "La cantidad no puede ser cero o negativa."}
            )
        return data

class ReporteProductoSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField()
    productos = ProductoSerializer(many=True)

class ContactSerializer(serializers.Serializer):
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=100,
                                    validators=[validar_subject])
    body = serializers.CharField(max_length=255)
