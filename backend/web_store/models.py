from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from donation_management.models import SampleType, Sample, Donor


class Product(models.Model):
    """Products available for purchase in the web store."""
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    sample_type = models.ForeignKey(SampleType, on_delete=models.CASCADE, related_name='products')
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    volume_ml = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    min_order_quantity = models.PositiveIntegerField(default=1)
    max_order_quantity = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.sku})"


class ProductAttribute(models.Model):
    """Attributes for products."""
    
    ATTRIBUTE_TYPE_CHOICES = (
        ('donor_age', 'Donor Age'),
        ('donor_sex', 'Donor Sex'),
        ('donor_ethnicity', 'Donor Ethnicity'),
        ('donor_blood_type', 'Donor Blood Type'),
        ('donor_hla', 'Donor HLA Type'),
        ('donor_health', 'Donor Health Status'),
        ('processing', 'Processing Method'),
        ('storage', 'Storage Condition'),
        ('other', 'Other'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute_type = models.CharField(max_length=20, choices=ATTRIBUTE_TYPE_CHOICES)
    attribute_name = models.CharField(max_length=255)
    attribute_value = models.CharField(max_length=255)
    is_filterable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('product', 'attribute_type', 'attribute_name')
    
    def __str__(self):
        return f"{self.product.name} - {self.attribute_name}: {self.attribute_value}"


class ProductInventory(models.Model):
    """Inventory for products."""
    
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    available_quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    last_inventory_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.name} - Available: {self.available_quantity}"


class ProductSample(models.Model):
    """Specific samples assigned to products."""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='samples')
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE, related_name='product')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.sample.sample_id}"


class InstitutionalBuyer(models.Model):
    """Approved institutional buyers."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='institutional_buyer')
    institution_name = models.CharField(max_length=255)
    institution_type = models.CharField(max_length=255)
    institution_address = models.TextField()
    tax_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verification_document = models.FileField(upload_to='buyer_verification/', blank=True, null=True)
    api_access_enabled = models.BooleanField(default=False)
    api_key = models.CharField(max_length=64, blank=True, null=True, unique=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.institution_name} - {self.user.full_name}"


class Cart(models.Model):
    """Shopping cart for users."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.full_name}"
    
    @property
    def total_items(self):
        return self.items.count()
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """Items in a shopping cart."""
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('cart', 'product')
    
    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) in {self.cart}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    """Orders from users."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('ach', 'ACH Transfer'),
        ('wire', 'Wire Transfer'),
        ('purchase_order', 'Purchase Order'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    shipping_address = models.TextField()
    shipping_method = models.CharField(max_length=100)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.user.full_name}"


class OrderItem(models.Model):
    """Items in an order."""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) in Order #{self.order.order_number}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)


class OrderSample(models.Model):
    """Specific samples assigned to order items."""
    
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='samples')
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='order_items')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('order_item', 'sample')
    
    def __str__(self):
        return f"Order #{self.order_item.order.order_number} - {self.sample.sample_id}"


class Invoice(models.Model):
    """Invoices for orders."""
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    issue_date = models.DateField()
    due_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Invoice #{self.invoice_number} for Order #{self.order.order_number}"


class APIKey(models.Model):
    """API keys for institutional buyers."""
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('revoked', 'Revoked'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    key = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    expires_at = models.DateTimeField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.full_name}"


class APIAccessLog(models.Model):
    """Access logs for API usage."""
    
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE, related_name='access_logs')
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.PositiveIntegerField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    request_data = models.JSONField(blank=True, null=True)
    response_data = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.api_key.user.full_name} - {self.endpoint} ({self.timestamp})"
