from django.test import TestCase
from django.utils import timezone
from web_store.models import (
    Product, ProductAttribute, ProductInventory, InstitutionalBuyer,
    Cart, CartItem, Order, OrderItem, Invoice, APIKey
)
from web_store.serializers import (
    ProductListSerializer, ProductDetailSerializer, ProductAttributeSerializer,
    ProductInventorySerializer, InstitutionalBuyerSerializer, CartSerializer,
    CartItemSerializer, OrderListSerializer, OrderDetailSerializer,
    InvoiceSerializer, APIKeySerializer
)
from users.models import User
from donation_management.models import SampleType

class WebStoreSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='buyer@example.com',
            password='password123',
            first_name='Test',
            last_name='Buyer',
            is_researcher=True
        )
        
        self.sample_type = SampleType.objects.create(
            name='Plasma',
            description='Blood plasma',
            storage_temperature='-20',
            shelf_life_days=365,
            processing_instructions='Centrifuge at 3000 rpm for 15 minutes',
            is_active=True
        )
        
        self.product = Product.objects.create(
            name='Plasma Sample',
            description='High-quality plasma sample',
            sample_type=self.sample_type,
            sku='PS-001',
            price=100.00,
            volume_ml=10,
            status='AVAILABLE',
            is_featured=True,
            min_order_quantity=1,
            max_order_quantity=10
        )
        
        self.product_attribute = ProductAttribute.objects.create(
            product=self.product,
            attribute_type='DONOR',
            attribute_name='Age',
            attribute_value='25-35',
            is_filterable=True
        )
        
        self.product_inventory = ProductInventory.objects.create(
            product=self.product,
            available_quantity=50,
            reserved_quantity=5
        )
        
        self.institutional_buyer = InstitutionalBuyer.objects.create(
            user=self.user,
            institution_name='Test University',
            institution_type='ACADEMIC',
            institution_address='123 University St, City',
            tax_id='12-3456789',
            status='APPROVED',
            api_access_enabled=True
        )
        
        self.cart = Cart.objects.create(
            user=self.user
        )
        
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        
        self.order = Order.objects.create(
            user=self.user,
            order_number='WS-001',
            status='PROCESSING',
            payment_status='PAID',
            payment_method='CREDIT_CARD',
            payment_id='ch_123456',
            shipping_address='123 University St, City',
            shipping_method='Express',
            shipping_cost=15.00,
            subtotal=200.00,
            tax=20.00,
            total=235.00
        )
        
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=100.00,
            total_price=200.00
        )
        
        self.invoice = Invoice.objects.create(
            order=self.order,
            invoice_number='INV-001',
            status='PAID',
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timezone.timedelta(days=30),
            payment_date=timezone.now().date(),
            subtotal=200.00,
            tax=20.00,
            shipping=15.00,
            total=235.00
        )
        
        self.api_key = APIKey.objects.create(
            user=self.user,
            key='test_api_key_123',
            name='Test API Key',
            status='ACTIVE',
            expires_at=timezone.now() + timezone.timedelta(days=365)
        )
    
    def test_product_list_serializer(self):
        serializer = ProductListSerializer(instance=self.product)
        data = serializer.data
        
        self.assertEqual(data['name'], self.product.name)
        self.assertEqual(data['sku'], self.product.sku)
        self.assertEqual(data['price'], str(self.product.price))
        self.assertEqual(data['volume_ml'], self.product.volume_ml)
        self.assertEqual(data['status'], self.product.status)
        self.assertTrue(data['is_featured'])
        
        self.assertEqual(data['sample_type']['name'], self.sample_type.name)
        
        self.assertEqual(data['inventory']['available_quantity'], self.product_inventory.available_quantity)
        self.assertEqual(data['inventory']['reserved_quantity'], self.product_inventory.reserved_quantity)
    
    def test_product_detail_serializer(self):
        serializer = ProductDetailSerializer(instance=self.product)
        data = serializer.data
        
        self.assertEqual(data['name'], self.product.name)
        self.assertEqual(data['description'], self.product.description)
        self.assertEqual(data['sku'], self.product.sku)
        self.assertEqual(data['price'], str(self.product.price))
        self.assertEqual(data['volume_ml'], self.product.volume_ml)
        self.assertEqual(data['status'], self.product.status)
        self.assertTrue(data['is_featured'])
        self.assertEqual(data['min_order_quantity'], self.product.min_order_quantity)
        self.assertEqual(data['max_order_quantity'], self.product.max_order_quantity)
        
        self.assertEqual(len(data['attributes']), 1)
        self.assertEqual(data['attributes'][0]['attribute_name'], self.product_attribute.attribute_name)
        self.assertEqual(data['attributes'][0]['attribute_value'], self.product_attribute.attribute_value)
    
    def test_product_attribute_serializer(self):
        serializer = ProductAttributeSerializer(instance=self.product_attribute)
        data = serializer.data
        
        self.assertEqual(data['attribute_type'], self.product_attribute.attribute_type)
        self.assertEqual(data['attribute_name'], self.product_attribute.attribute_name)
        self.assertEqual(data['attribute_value'], self.product_attribute.attribute_value)
        self.assertTrue(data['is_filterable'])
    
    def test_product_inventory_serializer(self):
        serializer = ProductInventorySerializer(instance=self.product_inventory)
        data = serializer.data
        
        self.assertEqual(data['available_quantity'], self.product_inventory.available_quantity)
        self.assertEqual(data['reserved_quantity'], self.product_inventory.reserved_quantity)
    
    def test_institutional_buyer_serializer(self):
        serializer = InstitutionalBuyerSerializer(instance=self.institutional_buyer)
        data = serializer.data
        
        self.assertEqual(data['institution_name'], self.institutional_buyer.institution_name)
        self.assertEqual(data['institution_type'], self.institutional_buyer.institution_type)
        self.assertEqual(data['institution_address'], self.institutional_buyer.institution_address)
        self.assertEqual(data['tax_id'], self.institutional_buyer.tax_id)
        self.assertEqual(data['status'], self.institutional_buyer.status)
        self.assertTrue(data['api_access_enabled'])
        
        self.assertEqual(data['user']['email'], self.user.email)
        self.assertEqual(data['user']['first_name'], self.user.first_name)
        self.assertEqual(data['user']['last_name'], self.user.last_name)
        
        self.assertNotIn('api_key', data)
    
    def test_cart_serializer(self):
        serializer = CartSerializer(instance=self.cart)
        data = serializer.data
        
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['quantity'], self.cart_item.quantity)
        
        self.assertEqual(data['user']['email'], self.user.email)
    
    def test_cart_item_serializer(self):
        serializer = CartItemSerializer(instance=self.cart_item)
        data = serializer.data
        
        self.assertEqual(data['quantity'], self.cart_item.quantity)
        
        self.assertEqual(data['product']['name'], self.product.name)
        self.assertEqual(data['product']['sku'], self.product.sku)
        self.assertEqual(data['product']['price'], str(self.product.price))
    
    def test_order_list_serializer(self):
        serializer = OrderListSerializer(instance=self.order)
        data = serializer.data
        
        self.assertEqual(data['order_number'], self.order.order_number)
        self.assertEqual(data['status'], self.order.status)
        self.assertEqual(data['payment_status'], self.order.payment_status)
        self.assertEqual(data['payment_method'], self.order.payment_method)
        self.assertEqual(data['total'], str(self.order.total))
        
        self.assertEqual(data['user']['email'], self.user.email)
    
    def test_order_detail_serializer(self):
        serializer = OrderDetailSerializer(instance=self.order)
        data = serializer.data
        
        self.assertEqual(data['order_number'], self.order.order_number)
        self.assertEqual(data['status'], self.order.status)
        self.assertEqual(data['payment_status'], self.order.payment_status)
        self.assertEqual(data['payment_method'], self.order.payment_method)
        self.assertEqual(data['payment_id'], self.order.payment_id)
        self.assertEqual(data['shipping_address'], self.order.shipping_address)
        self.assertEqual(data['shipping_method'], self.order.shipping_method)
        self.assertEqual(data['shipping_cost'], str(self.order.shipping_cost))
        self.assertEqual(data['subtotal'], str(self.order.subtotal))
        self.assertEqual(data['tax'], str(self.order.tax))
        self.assertEqual(data['total'], str(self.order.total))
        
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['quantity'], self.order_item.quantity)
        self.assertEqual(data['items'][0]['price'], str(self.order_item.price))
        self.assertEqual(data['items'][0]['total_price'], str(self.order_item.total_price))
        
        self.assertEqual(data['invoice']['invoice_number'], self.invoice.invoice_number)
        self.assertEqual(data['invoice']['status'], self.invoice.status)
    
    def test_invoice_serializer(self):
        serializer = InvoiceSerializer(instance=self.invoice)
        data = serializer.data
        
        self.assertEqual(data['invoice_number'], self.invoice.invoice_number)
        self.assertEqual(data['status'], self.invoice.status)
        self.assertEqual(data['subtotal'], str(self.invoice.subtotal))
        self.assertEqual(data['tax'], str(self.invoice.tax))
        self.assertEqual(data['shipping'], str(self.invoice.shipping))
        self.assertEqual(data['total'], str(self.invoice.total))
    
    def test_api_key_serializer(self):
        serializer = APIKeySerializer(instance=self.api_key)
        data = serializer.data
        
        self.assertEqual(data['name'], self.api_key.name)
        self.assertEqual(data['status'], self.api_key.status)
        
        self.assertNotIn('key', data)
        
        self.assertEqual(data['user']['email'], self.user.email)
