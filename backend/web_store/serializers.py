from rest_framework import serializers
from .models import (
    Product, ProductAttribute, ProductInventory, ProductSample,
    InstitutionalBuyer, Cart, CartItem, Order, OrderItem,
    OrderSample, Invoice, APIKey, APIAccessLog
)
from users.serializers import UserSerializer
from donation_management.serializers import SampleTypeSerializer, SampleSerializer


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = [
            'id', 'product', 'attribute_type', 'attribute_name',
            'attribute_value', 'is_filterable', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = [
            'id', 'product', 'available_quantity', 'reserved_quantity',
            'last_inventory_update'
        ]
        read_only_fields = ['last_inventory_update']


class ProductSampleSerializer(serializers.ModelSerializer):
    sample = SampleSerializer(read_only=True)
    
    class Meta:
        model = ProductSample
        fields = ['id', 'product', 'sample', 'is_available', 'created_at']
        read_only_fields = ['created_at']


class ProductListSerializer(serializers.ModelSerializer):
    sample_type = SampleTypeSerializer(read_only=True)
    inventory = ProductInventorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sample_type', 'sku', 'price', 'volume_ml',
            'status', 'image', 'is_featured', 'inventory', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    sample_type = SampleTypeSerializer(read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    inventory = ProductInventorySerializer(read_only=True)
    samples = ProductSampleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'sample_type', 'sku', 'price',
            'volume_ml', 'status', 'image', 'is_featured', 'min_order_quantity',
            'max_order_quantity', 'attributes', 'inventory', 'samples',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class InstitutionalBuyerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = InstitutionalBuyer
        fields = [
            'id', 'user', 'institution_name', 'institution_type',
            'institution_address', 'tax_id', 'status', 'verification_document',
            'api_access_enabled', 'api_key', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'api_key']
        extra_kwargs = {'api_key': {'write_only': True}}


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'cart', 'product', 'quantity', 'added_at', 'updated_at'
        ]
        read_only_fields = ['added_at', 'updated_at']
    
    def validate_quantity(self, value):
        product = self.instance.product if self.instance else self.initial_data.get('product')
        if product and value < product.min_order_quantity:
            raise serializers.ValidationError(
                f"Quantity must be at least {product.min_order_quantity}"
            )
        if product and product.max_order_quantity and value > product.max_order_quantity:
            raise serializers.ValidationError(
                f"Quantity cannot exceed {product.max_order_quantity}"
            )
        return value


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'items', 'total_items', 'total_price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'product', 'quantity', 'price',
            'total_price', 'created_at'
        ]
        read_only_fields = ['created_at', 'total_price']


class OrderSampleSerializer(serializers.ModelSerializer):
    sample = SampleSerializer(read_only=True)
    
    class Meta:
        model = OrderSample
        fields = ['id', 'order_item', 'sample', 'created_at']
        read_only_fields = ['created_at']


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'id', 'order', 'invoice_number', 'status', 'issue_date',
            'due_date', 'payment_date', 'subtotal', 'tax', 'shipping',
            'total', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class OrderListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'order_number', 'status', 'payment_status',
            'payment_method', 'total', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    invoice = InvoiceSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'order_number', 'status', 'payment_status',
            'payment_method', 'payment_id', 'shipping_address', 'shipping_method',
            'shipping_cost', 'tracking_number', 'subtotal', 'tax', 'total',
            'notes', 'items', 'invoice', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class APIKeySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = APIKey
        fields = [
            'id', 'user', 'key', 'name', 'status', 'expires_at',
            'last_used_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'last_used_at']
        extra_kwargs = {'key': {'write_only': True}}


class APIAccessLogSerializer(serializers.ModelSerializer):
    api_key = APIKeySerializer(read_only=True)
    
    class Meta:
        model = APIAccessLog
        fields = [
            'id', 'api_key', 'endpoint', 'method', 'status_code',
            'ip_address', 'user_agent', 'request_data', 'response_data',
            'timestamp'
        ]
        read_only_fields = ['timestamp']
