from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('pcs', 'Pieces'),
        ('kg', 'Kilograms'),
        ('lbs', 'Pounds'),
        ('liters', 'Liters'),
        ('meters', 'Meters'),
        ('boxes', 'Boxes'),
    ]
    
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pcs')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_point = models.PositiveIntegerField(default=10)
    reorder_quantity = models.PositiveIntegerField(default=50)
    barcode = models.CharField(max_length=100, blank=True, unique=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.sku} - {self.name}"
    
    @property
    def current_stock(self):
        return self.stock_records.aggregate(
            total=models.Sum('current_quantity')
        )['total'] or 0
    
    @property
    def needs_reorder(self):
        return self.current_stock <= self.reorder_point


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    address = models.TextField()
    manager = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(help_text='Storage capacity in units')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_records')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_records')
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reserved_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'warehouse']
        ordering = ['product__name']
    
    def __str__(self):
        return f"{self.product.name} @ {self.warehouse.name}: {self.current_quantity}"
    
    @property
    def available_quantity(self):
        return self.current_quantity - self.reserved_quantity


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),
        ('return', 'Return'),
        ('damage', 'Damaged'),
    ]
    
    movement_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.movement_type} - {self.product.name} - {self.quantity}"


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent to Supplier'),
        ('confirmed', 'Confirmed'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]
    
    po_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_orders')
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_by = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['-order_date']
    
    def __str__(self):
        return f"{self.po_number} - {self.supplier.name}"


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.product.name}"


class InventoryAlert(models.Model):
    ALERT_TYPES = [
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('overstock', 'Overstock'),
        ('expiry_warning', 'Expiry Warning'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='alerts')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.alert_type} - {self.product.name}"
