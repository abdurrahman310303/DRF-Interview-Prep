# Inventory Management API - DRF Interview Prep Project

## 🎯 Project Overview

A comprehensive Django REST Framework API for inventory and warehouse management that demonstrates:
- **Supply Chain Management** patterns
- **Stock Level Optimization** algorithms
- **Multi-location Inventory** tracking
- **Automated Reordering** systems
- **Barcode/QR Code Integration**
- **Advanced Reporting** and analytics

## 🚀 Features

### **Product Management**
- Product catalog with variants (size, color, model)
- SKU generation and barcode management
- Product categories and hierarchies
- Supplier and vendor management
- Product lifecycle tracking
- Multi-unit support (pieces, kg, liters, etc.)

### **Inventory Tracking**
- Real-time stock levels across multiple warehouses
- Stock movement history and audit trails
- Batch/lot tracking for perishable items
- Serial number tracking for high-value items
- Expiry date management
- Damaged/defective stock handling

### **Warehouse Management**
- Multiple warehouse/location support
- Bin/shelf location tracking
- Warehouse capacity management
- Transfer between locations
- Receiving and shipping workflows
- Cycle counting and physical inventory

### **Automated Systems**
- Low stock alerts and notifications
- Automatic reorder point calculation
- Purchase order generation
- Demand forecasting
- ABC analysis for inventory optimization
- Lead time tracking

### **Reporting & Analytics**
- Inventory valuation reports
- Stock movement analysis
- Turnover ratio calculations
- Dead stock identification
- Shortage and overage reports
- Cost analysis and profitability

## 🏗️ System Architecture

### **Database Models**
- **Product**: Core product information
- **ProductVariant**: Product variations
- **Warehouse**: Storage locations
- **Stock**: Current inventory levels
- **StockMovement**: All stock transactions
- **Supplier**: Vendor information
- **PurchaseOrder**: Procurement tracking
- **InventoryAlert**: Automated notifications

## 📁 Project Structure

```
08_inventory_management_api/
├── inventory_api/            # Main Django project
│   ├── settings.py           # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── products/                 # Product management app
│   ├── models.py            # Product, Variant models
│   ├── serializers.py       # Product serializers
│   ├── views.py             # Product ViewSets
│   ├── filters.py           # Product filters
│   └── admin.py             # Admin interface
├── inventory/                # Inventory tracking app
│   ├── models.py            # Stock, Movement models
│   ├── serializers.py       # Inventory serializers
│   ├── views.py             # Inventory ViewSets
│   ├── utils.py             # Inventory calculations
│   └── admin.py             # Admin interface
├── warehouses/               # Warehouse management app
│   ├── models.py            # Warehouse, Location models
│   ├── serializers.py       # Warehouse serializers
│   ├── views.py             # Warehouse ViewSets
│   └── admin.py             # Admin interface
├── suppliers/                # Supplier management app
│   ├── models.py            # Supplier models
│   ├── serializers.py       # Supplier serializers
│   ├── views.py             # Supplier ViewSets
│   └── admin.py             # Admin interface
├── orders/                   # Purchase order app
│   ├── models.py            # PurchaseOrder models
│   ├── serializers.py       # Order serializers
│   ├── views.py             # Order ViewSets
│   ├── workflows.py         # Order workflows
│   └── admin.py             # Admin interface
├── analytics/                # Analytics and reporting app
│   ├── views.py             # Report generation
│   ├── serializers.py       # Analytics serializers
│   ├── calculations.py      # Business calculations
│   └── tasks.py             # Background tasks
├── alerts/                   # Alert system app
│   ├── models.py            # Alert models
│   ├── tasks.py             # Celery tasks
│   └── notifications.py     # Notification handlers
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🛠️ Installation & Setup

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Environment Variables**
Create `.env` file:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost/inventory_db
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### **3. Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **4. Load Sample Data**
```bash
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/warehouses.json
python manage.py loaddata fixtures/suppliers.json
python manage.py loaddata fixtures/sample_products.json
```

### **5. Start Background Services**
```bash
# Terminal 1 - Redis
redis-server

# Terminal 2 - Celery Worker
celery -A inventory_api worker -l info

# Terminal 3 - Celery Beat
celery -A inventory_api beat -l info
```

### **6. Run Development Server**
```bash
python manage.py runserver
```

## 🌐 API Endpoints

### **Products**
- `GET /api/products/` - List products with filtering
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product
- `GET /api/products/search/?q=query` - Search products
- `GET /api/products/{id}/variants/` - Get product variants
- `POST /api/products/{id}/generate-sku/` - Generate SKU

### **Inventory**
- `GET /api/inventory/` - List inventory levels
- `GET /api/inventory/stock-levels/` - Current stock summary
- `GET /api/inventory/{product_id}/` - Product inventory details
- `POST /api/inventory/adjust/` - Adjust stock levels
- `GET /api/inventory/movements/` - Stock movement history
- `GET /api/inventory/low-stock/` - Low stock items
- `GET /api/inventory/out-of-stock/` - Out of stock items

### **Warehouses**
- `GET /api/warehouses/` - List warehouses
- `POST /api/warehouses/` - Create new warehouse
- `GET /api/warehouses/{id}/` - Get warehouse details
- `GET /api/warehouses/{id}/inventory/` - Warehouse inventory
- `POST /api/warehouses/transfer/` - Transfer between warehouses
- `GET /api/warehouses/{id}/capacity/` - Warehouse capacity

### **Stock Movements**
- `GET /api/movements/` - List stock movements
- `POST /api/movements/receive/` - Receive stock
- `POST /api/movements/issue/` - Issue stock
- `POST /api/movements/return/` - Return stock
- `POST /api/movements/adjust/` - Stock adjustment
- `GET /api/movements/{id}/` - Movement details

### **Purchase Orders**
- `GET /api/purchase-orders/` - List purchase orders
- `POST /api/purchase-orders/` - Create purchase order
- `GET /api/purchase-orders/{id}/` - PO details
- `PUT /api/purchase-orders/{id}/approve/` - Approve PO
- `POST /api/purchase-orders/{id}/receive/` - Receive goods
- `GET /api/purchase-orders/pending/` - Pending approvals

### **Suppliers**
- `GET /api/suppliers/` - List suppliers
- `POST /api/suppliers/` - Add new supplier
- `GET /api/suppliers/{id}/` - Supplier details
- `GET /api/suppliers/{id}/products/` - Supplier's products
- `GET /api/suppliers/{id}/orders/` - Orders from supplier
- `GET /api/suppliers/{id}/performance/` - Supplier performance

### **Analytics & Reports**
- `GET /api/analytics/inventory-value/` - Total inventory value
- `GET /api/analytics/turnover-ratio/` - Inventory turnover
- `GET /api/analytics/abc-analysis/` - ABC classification
- `GET /api/analytics/dead-stock/` - Slow-moving items
- `GET /api/analytics/demand-forecast/` - Demand prediction
- `GET /api/reports/stock-aging/` - Stock aging report
- `GET /api/reports/movement-summary/` - Movement summary

### **Alerts**
- `GET /api/alerts/` - List active alerts
- `POST /api/alerts/acknowledge/` - Acknowledge alert
- `GET /api/alerts/low-stock/` - Low stock alerts
- `GET /api/alerts/expiry/` - Expiry alerts
- `PUT /api/alerts/settings/` - Configure alert thresholds

## 📊 Data Models

### **Product Model**
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    brand = models.CharField(max_length=100, blank=True)
    unit_of_measure = models.CharField(max_length=20)  # pieces, kg, liters
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_stock_level = models.IntegerField(default=0)
    maximum_stock_level = models.IntegerField(default=1000)
    reorder_point = models.IntegerField(default=10)
    reorder_quantity = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **Stock Model**
```python
class Stock(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    quantity_on_hand = models.IntegerField(default=0)
    quantity_reserved = models.IntegerField(default=0)  # Allocated but not shipped
    quantity_available = models.GeneratedField(  # Available = On Hand - Reserved
        expression=F('quantity_on_hand') - F('quantity_reserved'),
        output_field=models.IntegerField()
    )
    batch_number = models.CharField(max_length=50, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=50, blank=True)  # Bin/Shelf location
    last_counted = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['product', 'warehouse', 'batch_number']
```

### **StockMovement Model**
```python
class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('receive', 'Receive'),
        ('issue', 'Issue'),
        ('transfer', 'Transfer'),
        ('adjust', 'Adjustment'),
        ('return', 'Return'),
        ('damaged', 'Damaged'),
    ]
    
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()  # Positive for inbound, negative for outbound
    reference_number = models.CharField(max_length=50)  # PO number, invoice, etc.
    notes = models.TextField(blank=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    batch_number = models.CharField(max_length=50, blank=True)
```

### **PurchaseOrder Model**
```python
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent to Supplier'),
        ('confirmed', 'Confirmed'),
        ('partial', 'Partially Received'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    po_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    order_date = models.DateField(auto_now_add=True)
    expected_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, 
                                  related_name='approved_pos', null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
```

## 🧪 Testing the API

### **1. Create Product**
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse",
    "sku": "WM-001",
    "barcode": "1234567890123",
    "description": "Optical wireless mouse",
    "category": 1,
    "brand": "TechBrand",
    "unit_of_measure": "pieces",
    "cost_price": "25.00",
    "selling_price": "45.00",
    "minimum_stock_level": 10,
    "reorder_point": 20,
    "reorder_quantity": 50
  }'
```

### **2. Adjust Stock**
```bash
curl -X POST http://localhost:8000/api/inventory/adjust/ \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "warehouse": 1,
    "quantity": 100,
    "movement_type": "receive",
    "reference_number": "PO-001",
    "notes": "Initial stock receiving",
    "unit_cost": "25.00"
  }'
```

### **3. Create Purchase Order**
```bash
curl -X POST http://localhost:8000/api/purchase-orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "supplier": 1,
    "warehouse": 1,
    "expected_date": "2024-02-15",
    "items": [
      {
        "product": 1,
        "quantity": 50,
        "unit_price": "25.00"
      },
      {
        "product": 2,
        "quantity": 30,
        "unit_price": "15.00"
      }
    ],
    "notes": "Urgent restock order"
  }'
```

## 🔍 Advanced Features

### **Automated Reordering**
- Automatic PO generation when stock hits reorder point
- Economic Order Quantity (EOQ) calculations
- Lead time consideration
- Seasonal demand adjustments
- Supplier performance-based ordering

### **Analytics & Intelligence**
- ABC analysis for inventory classification
- Demand forecasting using historical data
- Stock aging analysis
- Turnover ratio calculations
- Dead stock identification

### **Integration Ready**
- Barcode/QR code scanning API
- ERP system integration endpoints
- E-commerce platform sync
- Accounting system integration
- Shipping carrier APIs

## 📈 Business Logic

### **Reorder Point Calculation**
```
Reorder Point = (Average Daily Usage × Lead Time Days) + Safety Stock
```

### **Economic Order Quantity**
```
EOQ = √(2 × Annual Demand × Ordering Cost / Holding Cost per Unit)
```

### **Inventory Turnover**
```
Turnover Ratio = Cost of Goods Sold / Average Inventory Value
```

### **ABC Classification**
- **A Items**: Top 20% of products by value (80% of total value)
- **B Items**: Next 30% of products (15% of total value)
- **C Items**: Remaining 50% of products (5% of total value)

## 🚀 Next Steps & Enhancements

### **Immediate Improvements**
1. **Mobile App** for warehouse operations
2. **Barcode Scanning** integration
3. **Advanced Forecasting** with ML
4. **Multi-currency Support**

### **Advanced Features**
1. **IoT Integration** for real-time tracking
2. **Blockchain** for supply chain transparency
3. **AI-powered Demand Planning**
4. **Drone-based Inventory Counting**
5. **Voice-activated Warehouse Operations**

## 🎓 Learning Outcomes

This project demonstrates:
- **Complex Business Logic** for inventory management
- **Supply Chain Management** concepts
- **Automated Systems** and background tasks
- **Advanced Analytics** and reporting
- **Multi-location Architecture**
- **Financial Calculations** and cost tracking
- **Performance Optimization** for high-volume data
- **Integration Patterns** with external systems

## 💡 Interview Topics Covered

- **Complex database relationships** and constraints
- **Automated business processes** with Celery
- **Financial calculations** and cost management
- **Performance optimization** for analytics queries
- **Data consistency** in multi-location systems
- **Background task processing**
- **Real-time notifications** and alerts
- **Reporting and data analysis** techniques

---

**Perfect for demonstrating enterprise-level inventory management system skills!** 📦
