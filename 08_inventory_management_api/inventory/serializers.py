from rest_framework import serializers
from .models import (
    Product, Category, Supplier, Warehouse, Stock, StockMovement,
    PurchaseOrder, PurchaseOrderItem, InventoryAlert
)


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'subcategories', 'products_count']
    
    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data
    
    def get_products_count(self, obj):
        return obj.products.count()


class SupplierSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'contact_person', 'email', 'phone', 'address',
            'is_active', 'products_count', 'created_at'
        ]
    
    def get_products_count(self, obj):
        return obj.products.count()


class WarehouseSerializer(serializers.ModelSerializer):
    current_capacity = serializers.SerializerMethodField()
    
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'code', 'address', 'manager', 'capacity', 'current_capacity', 'is_active']
    
    def get_current_capacity(self, obj):
        return obj.stock_records.aggregate(
            total=serializers.Sum('current_quantity')
        )['total'] or 0


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    supplier = SupplierSerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    supplier_id = serializers.IntegerField(write_only=True)
    current_stock = serializers.ReadOnlyField()
    needs_reorder = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'name', 'description', 'category', 'category_id',
            'supplier', 'supplier_id', 'unit', 'cost_price', 'selling_price',
            'reorder_point', 'reorder_quantity', 'barcode', 'image', 'is_active',
            'current_stock', 'needs_reorder', 'created_at', 'updated_at'
        ]


class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    warehouse_id = serializers.IntegerField(write_only=True)
    available_quantity = serializers.ReadOnlyField()
    
    class Meta:
        model = Stock
        fields = [
            'id', 'product', 'product_id', 'warehouse', 'warehouse_id',
            'current_quantity', 'reserved_quantity', 'available_quantity',
            'last_updated'
        ]


class StockMovementSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    warehouse_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = StockMovement
        fields = [
            'id', 'movement_id', 'product', 'product_id', 'warehouse', 'warehouse_id',
            'movement_type', 'quantity', 'reference_number', 'notes',
            'created_by', 'created_at'
        ]
    
    def create(self, validated_data):
        movement = super().create(validated_data)
        
        # Update stock based on movement type
        stock, created = Stock.objects.get_or_create(
            product=movement.product,
            warehouse=movement.warehouse
        )
        
        if movement.movement_type == 'in':
            stock.current_quantity += movement.quantity
        elif movement.movement_type == 'out':
            stock.current_quantity -= movement.quantity
        elif movement.movement_type == 'adjustment':
            # For adjustments, quantity can be positive or negative
            stock.current_quantity += movement.quantity
        
        stock.save()
        
        return movement


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = PurchaseOrderItem
        fields = [
            'id', 'product', 'product_id', 'quantity', 'unit_price', 'total_price'
        ]
        read_only_fields = ['total_price']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.IntegerField(write_only=True)
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    items_data = PurchaseOrderItemSerializer(many=True, write_only=True, required=False)
    
    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'po_number', 'supplier', 'supplier_id', 'order_date',
            'expected_delivery', 'status', 'total_amount', 'notes',
            'created_by', 'items', 'items_data'
        ]
        read_only_fields = ['order_date', 'total_amount']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items_data', [])
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        
        # Create PO items
        total = 0
        for item_data in items_data:
            item = PurchaseOrderItem.objects.create(
                purchase_order=purchase_order,
                **item_data
            )
            total += item.total_price
        
        purchase_order.total_amount = total
        purchase_order.save()
        
        return purchase_order


class InventoryAlertSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)
    
    class Meta:
        model = InventoryAlert
        fields = [
            'id', 'product', 'warehouse', 'alert_type', 'message',
            'is_resolved', 'created_at', 'resolved_at'
        ]


class InventoryReportSerializer(serializers.Serializer):
    total_products = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    total_suppliers = serializers.IntegerField()
    total_warehouses = serializers.IntegerField()
    low_stock_products = serializers.IntegerField()
    out_of_stock_products = serializers.IntegerField()
    total_stock_value = serializers.DecimalField(max_digits=15, decimal_places=2)
