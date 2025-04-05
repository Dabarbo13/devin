import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from .models import (
    Product, ProductAttribute, ProductInventory, InstitutionalBuyer,
    Cart, CartItem, Order, OrderItem, Invoice, APIKey
)

User = get_user_model()

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class ProductAttributeType(DjangoObjectType):
    class Meta:
        model = ProductAttribute

class ProductInventoryType(DjangoObjectType):
    class Meta:
        model = ProductInventory

class InstitutionalBuyerType(DjangoObjectType):
    class Meta:
        model = InstitutionalBuyer
        exclude = ('api_key',)

class CartType(DjangoObjectType):
    class Meta:
        model = Cart

class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem

class InvoiceType(DjangoObjectType):
    class Meta:
        model = Invoice

class APIKeyType(DjangoObjectType):
    class Meta:
        model = APIKey
        exclude = ('key',)

class Query(graphene.ObjectType):
    products = graphene.List(
        ProductType,
        sample_type_id=graphene.ID(),
        status=graphene.String(),
        is_featured=graphene.Boolean()
    )
    product = graphene.Field(ProductType, id=graphene.ID(required=True))
    
    product_attributes = graphene.List(
        ProductAttributeType,
        product_id=graphene.ID(),
        attribute_type=graphene.String(),
        is_filterable=graphene.Boolean()
    )
    product_attribute = graphene.Field(ProductAttributeType, id=graphene.ID(required=True))
    
    product_inventories = graphene.List(
        ProductInventoryType,
        product_id=graphene.ID()
    )
    product_inventory = graphene.Field(ProductInventoryType, id=graphene.ID(required=True))
    
    institutional_buyers = graphene.List(
        InstitutionalBuyerType,
        institution_type=graphene.String(),
        status=graphene.String()
    )
    institutional_buyer = graphene.Field(InstitutionalBuyerType, id=graphene.ID(required=True))
    my_institutional_buyer = graphene.Field(InstitutionalBuyerType)
    
    my_cart = graphene.Field(CartType)
    
    orders = graphene.List(
        OrderType,
        user_id=graphene.ID(),
        status=graphene.String(),
        payment_status=graphene.String()
    )
    order = graphene.Field(OrderType, id=graphene.ID(required=True))
    my_orders = graphene.List(OrderType, status=graphene.String())
    
    invoices = graphene.List(
        InvoiceType,
        order_id=graphene.ID(),
        status=graphene.String()
    )
    invoice = graphene.Field(InvoiceType, id=graphene.ID(required=True))
    
    my_api_keys = graphene.List(APIKeyType, status=graphene.String())
    
    def resolve_products(self, info, sample_type_id=None, status=None, is_featured=None):
        query = Product.objects.all()
        
        if sample_type_id:
            query = query.filter(sample_type_id=sample_type_id)
        if status:
            query = query.filter(status=status)
        else:
            query = query.filter(status='AVAILABLE')
        if is_featured is not None:
            query = query.filter(is_featured=is_featured)
        
        return query
    
    def resolve_product(self, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            raise GraphQLError('Product not found')
    
    def resolve_product_attributes(self, info, product_id=None, attribute_type=None, is_filterable=None):
        query = ProductAttribute.objects.all()
        
        if product_id:
            query = query.filter(product_id=product_id)
        if attribute_type:
            query = query.filter(attribute_type=attribute_type)
        if is_filterable is not None:
            query = query.filter(is_filterable=is_filterable)
        
        return query
    
    def resolve_product_attribute(self, info, id):
        try:
            return ProductAttribute.objects.get(pk=id)
        except ProductAttribute.DoesNotExist:
            raise GraphQLError('Product attribute not found')
    
    def resolve_product_inventories(self, info, product_id=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view product inventories')
        
        user = info.context.user
        
        if not (user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to view product inventories')
        
        query = ProductInventory.objects.all()
        
        if product_id:
            query = query.filter(product_id=product_id)
        
        return query
    
    def resolve_product_inventory(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view product inventory details')
        
        user = info.context.user
        
        if not (user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to view product inventory details')
        
        try:
            return ProductInventory.objects.get(pk=id)
        except ProductInventory.DoesNotExist:
            raise GraphQLError('Product inventory not found')
    
    def resolve_institutional_buyers(self, info, institution_type=None, status=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view institutional buyers')
        
        user = info.context.user
        
        if not (user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to view institutional buyers')
        
        query = InstitutionalBuyer.objects.all()
        
        if institution_type:
            query = query.filter(institution_type=institution_type)
        if status:
            query = query.filter(status=status)
        
        return query
    
    def resolve_institutional_buyer(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view institutional buyer details')
        
        try:
            buyer = InstitutionalBuyer.objects.get(pk=id)
            user = info.context.user
            
            if user.is_staff or user.is_superuser:
                return buyer
            
            if buyer.user == user:
                return buyer
            
            raise GraphQLError('You do not have permission to view this institutional buyer')
        except InstitutionalBuyer.DoesNotExist:
            raise GraphQLError('Institutional buyer not found')
    
    def resolve_my_institutional_buyer(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view your institutional buyer profile')
        
        user = info.context.user
        
        try:
            return InstitutionalBuyer.objects.get(user=user)
        except InstitutionalBuyer.DoesNotExist:
            raise GraphQLError('Institutional buyer profile not found')
    
    def resolve_my_cart(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view your cart')
        
        user = info.context.user
        
        cart, created = Cart.objects.get_or_create(user=user)
        
        return cart
    
    def resolve_orders(self, info, user_id=None, status=None, payment_status=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view orders')
        
        user = info.context.user
        
        if not (user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to view all orders')
        
        query = Order.objects.all()
        
        if user_id:
            query = query.filter(user_id=user_id)
        if status:
            query = query.filter(status=status)
        if payment_status:
            query = query.filter(payment_status=payment_status)
        
        return query
    
    def resolve_order(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view order details')
        
        try:
            order = Order.objects.get(pk=id)
            user = info.context.user
            
            if user.is_staff or user.is_superuser:
                return order
            
            if order.user == user:
                return order
            
            raise GraphQLError('You do not have permission to view this order')
        except Order.DoesNotExist:
            raise GraphQLError('Order not found')
    
    def resolve_my_orders(self, info, status=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view your orders')
        
        user = info.context.user
        
        query = Order.objects.filter(user=user)
        
        if status:
            query = query.filter(status=status)
        
        return query
    
    def resolve_invoices(self, info, order_id=None, status=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view invoices')
        
        user = info.context.user
        
        if not (user.is_staff or user.is_superuser):
            raise GraphQLError('You do not have permission to view all invoices')
        
        query = Invoice.objects.all()
        
        if order_id:
            query = query.filter(order_id=order_id)
        if status:
            query = query.filter(status=status)
        
        return query
    
    def resolve_invoice(self, info, id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view invoice details')
        
        try:
            invoice = Invoice.objects.get(pk=id)
            user = info.context.user
            
            if user.is_staff or user.is_superuser:
                return invoice
            
            if invoice.order.user == user:
                return invoice
            
            raise GraphQLError('You do not have permission to view this invoice')
        except Invoice.DoesNotExist:
            raise GraphQLError('Invoice not found')
    
    def resolve_my_api_keys(self, info, status=None):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to view your API keys')
        
        user = info.context.user
        
        query = APIKey.objects.filter(user=user)
        
        if status:
            query = query.filter(status=status)
        
        return query

class CartItemInput(graphene.InputObjectType):
    product_id = graphene.ID(required=True)
    quantity = graphene.Int(required=True)

class InstitutionalBuyerInput(graphene.InputObjectType):
    institution_name = graphene.String(required=True)
    institution_type = graphene.String(required=True)
    institution_address = graphene.String(required=True)
    tax_id = graphene.String(required=True)
    api_access_enabled = graphene.Boolean()

class OrderInput(graphene.InputObjectType):
    shipping_address = graphene.String(required=True)
    shipping_method = graphene.String(required=True)
    payment_method = graphene.String(required=True)

class APIKeyInput(graphene.InputObjectType):
    name = graphene.String(required=True)

class AddToCart(graphene.Mutation):
    class Arguments:
        input = CartItemInput(required=True)
    
    cart = graphene.Field(CartType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to add items to your cart')
        
        user = info.context.user
        
        cart, created = Cart.objects.get_or_create(user=user)
        
        try:
            product = Product.objects.get(pk=input.product_id)
        except Product.DoesNotExist:
            raise GraphQLError('Product not found')
        
        if product.status != 'AVAILABLE':
            raise GraphQLError('Product is not available')
        
        try:
            inventory = ProductInventory.objects.get(product=product)
            if inventory.available_quantity < input.quantity:
                raise GraphQLError('Not enough inventory available')
        except ProductInventory.DoesNotExist:
            raise GraphQLError('Product inventory not found')
        
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity = input.quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=input.quantity
            )
        
        return AddToCart(cart=cart)

class RemoveFromCart(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)
    
    cart = graphene.Field(CartType)
    
    @staticmethod
    def mutate(root, info, product_id):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to remove items from your cart')
        
        user = info.context.user
        
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise GraphQLError('Cart not found')
        
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise GraphQLError('Product not found')
        
        CartItem.objects.filter(cart=cart, product=product).delete()
        
        return RemoveFromCart(cart=cart)

class CreateInstitutionalBuyer(graphene.Mutation):
    class Arguments:
        input = InstitutionalBuyerInput(required=True)
    
    institutional_buyer = graphene.Field(InstitutionalBuyerType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create an institutional buyer profile')
        
        user = info.context.user
        
        if InstitutionalBuyer.objects.filter(user=user).exists():
            raise GraphQLError('You already have an institutional buyer profile')
        
        buyer = InstitutionalBuyer.objects.create(
            user=user,
            institution_name=input.institution_name,
            institution_type=input.institution_type,
            institution_address=input.institution_address,
            tax_id=input.tax_id,
            status='PENDING',
            api_access_enabled=getattr(input, 'api_access_enabled', False)
        )
        
        return CreateInstitutionalBuyer(institutional_buyer=buyer)

class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)
    
    order = graphene.Field(OrderType)
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create an order')
        
        user = info.context.user
        
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise GraphQLError('Cart not found')
        
        if not cart.cartitem_set.exists():
            raise GraphQLError('Cart is empty')
        
        subtotal = 0
        for item in cart.cartitem_set.all():
            subtotal += item.product.price * item.quantity
        
        tax = subtotal * 0.1
        
        if input.shipping_method == 'Standard':
            shipping_cost = 10.00
        elif input.shipping_method == 'Express':
            shipping_cost = 20.00
        else:
            shipping_cost = 15.00
        
        total = subtotal + tax + shipping_cost
        
        import random
        import string
        order_number = 'WS-' + ''.join(random.choices(string.digits, k=6))
        
        order = Order.objects.create(
            user=user,
            order_number=order_number,
            status='PROCESSING',
            payment_status='PENDING',
            payment_method=input.payment_method,
            shipping_address=input.shipping_address,
            shipping_method=input.shipping_method,
            shipping_cost=shipping_cost,
            subtotal=subtotal,
            tax=tax,
            total=total
        )
        
        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                total_price=cart_item.product.price * cart_item.quantity
            )
            
            try:
                inventory = ProductInventory.objects.get(product=cart_item.product)
                inventory.available_quantity -= cart_item.quantity
                inventory.reserved_quantity += cart_item.quantity
                inventory.save()
            except ProductInventory.DoesNotExist:
                pass
        
        from django.utils import timezone
        Invoice.objects.create(
            order=order,
            invoice_number='INV-' + order_number[3:],
            status='PENDING',
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timezone.timedelta(days=30),
            subtotal=subtotal,
            tax=tax,
            shipping=shipping_cost,
            total=total
        )
        
        cart.cartitem_set.all().delete()
        
        return CreateOrder(order=order)

class CreateAPIKey(graphene.Mutation):
    class Arguments:
        input = APIKeyInput(required=True)
    
    api_key = graphene.Field(APIKeyType)
    key = graphene.String()
    
    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('You must be logged in to create an API key')
        
        user = info.context.user
        
        try:
            buyer = InstitutionalBuyer.objects.get(user=user)
            if not buyer.api_access_enabled:
                raise GraphQLError('API access is not enabled for your account')
            if buyer.status != 'APPROVED':
                raise GraphQLError('Your institutional buyer account must be approved to create API keys')
        except InstitutionalBuyer.DoesNotExist:
            raise GraphQLError('You must have an institutional buyer profile to create API keys')
        
        import secrets
        key = secrets.token_urlsafe(32)
        
        from django.utils import timezone
        api_key = APIKey.objects.create(
            user=user,
            key=key,  # This would be hashed in a real application
            name=input.name,
            status='ACTIVE',
            expires_at=timezone.now() + timezone.timedelta(days=365)
        )
        
        return CreateAPIKey(api_key=api_key, key=key)

class Mutation(graphene.ObjectType):
    add_to_cart = AddToCart.Field()
    remove_from_cart = RemoveFromCart.Field()
    create_institutional_buyer = CreateInstitutionalBuyer.Field()
    create_order = CreateOrder.Field()
    create_api_key = CreateAPIKey.Field()
