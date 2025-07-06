# Expense Tracker API - DRF Interview Prep Project

## 🎯 Project Overview

A comprehensive personal finance Django REST Framework API that demonstrates:
- **Financial Data Modeling** with categories and budgets
- **Aggregation and Analytics** with Django ORM
- **Date-based Filtering** and time-series data
- **Data Validation** for financial transactions
- **Report Generation** with different time periods
- **Budget Management and Alerts**

## 🚀 Features

### **Expense Management**
- Add, edit, delete expenses
- Categorize expenses (Food, Transport, Entertainment, etc.)
- Recurring expense support
- Receipt image upload
- Multiple payment methods (Cash, Card, UPI, etc.)

### **Income Tracking**
- Record income from various sources
- Salary, freelance, investment income
- Regular income scheduling
- Income categorization

### **Budget Management**
- Set monthly/yearly budgets per category
- Budget vs actual spending comparison
- Budget alerts and notifications
- Budget rollover options

### **Analytics & Reports**
- Monthly/weekly spending summaries
- Category-wise expense breakdown
- Income vs expense analysis
- Spending trends over time
- Export reports to CSV/PDF

### **Smart Features**
- Expense prediction based on history
- Budget recommendations
- Spending pattern analysis
- Goal-based savings tracking

## 🏗️ System Architecture

### **Database Models**
- **Category**: Expense/Income categories
- **Expense**: Individual expense records
- **Income**: Income tracking
- **Budget**: Budget planning per category
- **PaymentMethod**: Different payment options
- **RecurringTransaction**: Template for recurring items

## 📁 Project Structure

```
05_expense_tracker_api/
├── expense_api/              # Main Django project
│   ├── settings.py           # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── transactions/             # Transaction management app
│   ├── models.py            # Expense, Income models
│   ├── serializers.py       # Transaction serializers
│   ├── views.py             # Transaction ViewSets
│   ├── filters.py           # Custom filters
│   └── admin.py             # Admin interface
├── categories/               # Category management app
│   ├── models.py            # Category model
│   ├── serializers.py       # Category serializers
│   ├── views.py             # Category ViewSet
│   └── admin.py             # Admin interface
├── budgets/                  # Budget management app
│   ├── models.py            # Budget model
│   ├── serializers.py       # Budget serializers
│   ├── views.py             # Budget ViewSet
│   ├── utils.py             # Budget calculations
│   └── admin.py             # Admin interface
├── reports/                  # Reporting app
│   ├── views.py             # Report generation
│   ├── serializers.py       # Report serializers
│   └── utils.py             # Report utilities
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🛠️ Installation & Setup

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **3. Load Sample Data**
```bash
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/payment_methods.json
```

### **4. Create Superuser**
```bash
python manage.py createsuperuser
```

### **5. Run Development Server**
```bash
python manage.py runserver
```

## 🌐 API Endpoints

### **Expenses**
- `GET /api/expenses/` - List expenses with filtering
- `POST /api/expenses/` - Add new expense
- `GET /api/expenses/{id}/` - Get expense details
- `PUT /api/expenses/{id}/` - Update expense
- `DELETE /api/expenses/{id}/` - Delete expense
- `GET /api/expenses/monthly/` - Monthly expense summary
- `POST /api/expenses/bulk/` - Bulk expense import

### **Income**
- `GET /api/income/` - List income records
- `POST /api/income/` - Add new income
- `GET /api/income/{id}/` - Get income details
- `PUT /api/income/{id}/` - Update income
- `DELETE /api/income/{id}/` - Delete income
- `GET /api/income/monthly/` - Monthly income summary

### **Categories**
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create new category
- `GET /api/categories/{id}/` - Get category details
- `GET /api/categories/{id}/expenses/` - Get category expenses
- `GET /api/categories/stats/` - Category spending statistics

### **Budgets**
- `GET /api/budgets/` - List budgets
- `POST /api/budgets/` - Create new budget
- `GET /api/budgets/{id}/` - Get budget details
- `PUT /api/budgets/{id}/` - Update budget
- `GET /api/budgets/current/` - Current month budgets
- `GET /api/budgets/alerts/` - Budget overspend alerts

### **Reports**
- `GET /api/reports/summary/` - Financial summary
- `GET /api/reports/monthly/` - Monthly report
- `GET /api/reports/category/` - Category breakdown
- `GET /api/reports/trends/` - Spending trends
- `GET /api/reports/export/` - Export data (CSV/PDF)

## 🔐 Business Rules

### **Expense Validation**
- Amount must be positive
- Date cannot be in future (configurable)
- Category is mandatory
- Receipt upload optional but recommended

### **Budget Rules**
- Budget amount must be positive
- Budget period (monthly/yearly)
- Alert thresholds (50%, 80%, 100%)
- Rollover unused budget option

### **Recurring Transactions**
- Support for daily, weekly, monthly, yearly
- End date or occurrence count
- Auto-creation with notifications

## 📊 Data Models

### **Expense Model**
```python
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE)
    date = models.DateField()
    receipt = models.ImageField(upload_to='receipts/', blank=True)
    is_recurring = models.BooleanField(default=False)
    recurring_template = models.ForeignKey('RecurringTransaction', 
                                         on_delete=models.CASCADE, 
                                         null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **Budget Model**
```python
class Budget(models.Model):
    PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    alert_threshold = models.IntegerField(default=80)  # Percentage
    rollover_unused = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
```

### **Category Model**
```python
class Category(models.Model):
    CATEGORY_TYPES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#3498db')  # Hex color
    icon = models.CharField(max_length=50, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, 
                              null=True, blank=True)
    is_active = models.BooleanField(default=True)
```

## 🧪 Testing the API

### **1. Add Expense**
```bash
curl -X POST http://localhost:8000/api/expenses/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "150.00",
    "description": "Lunch at restaurant",
    "category": 1,
    "payment_method": 2,
    "date": "2024-01-15"
  }'
```

### **2. Set Budget**
```bash
curl -X POST http://localhost:8000/api/budgets/ \
  -H "Content-Type: application/json" \
  -d '{
    "category": 1,
    "amount": "5000.00",
    "period": "monthly",
    "start_date": "2024-01-01",
    "alert_threshold": 80
  }'
```

### **3. Get Monthly Report**
```bash
curl -X GET "http://localhost:8000/api/reports/monthly/?month=2024-01"
```

## 🔍 Advanced Features

### **Smart Analytics**
- Spending pattern recognition
- Unusual spending alerts
- Seasonal spending analysis
- Goal-based savings tracking

### **Data Visualization Ready**
- JSON responses optimized for charts
- Time-series data formatting
- Category breakdowns
- Trend analysis data

### **Import/Export**
- CSV import for bulk transactions
- Bank statement parsing
- Data export in multiple formats
- Backup and restore functionality

## 📈 Filtering & Search

### **Date Filtering**
- Filter by date range: `?date_after=2024-01-01&date_before=2024-01-31`
- Filter by month: `?month=2024-01`
- Filter by year: `?year=2024`

### **Amount Filtering**
- Filter by amount range: `?min_amount=100&max_amount=1000`
- Filter by category: `?category=1`
- Filter by payment method: `?payment_method=2`

### **Search**
- Search descriptions: `?search=restaurant`
- Search by category name: `?category_name=food`

## 🚀 Next Steps & Enhancements

### **Immediate Improvements**
1. **Mobile App Integration** with receipt scanning
2. **Bank Integration** for automatic transaction import
3. **Advanced Reporting** with charts and graphs
4. **Multi-currency Support**

### **Advanced Features**
1. **Machine Learning** for expense categorization
2. **Investment Tracking** integration
3. **Bill Reminders** and notifications
4. **Financial Goals** and milestone tracking
5. **Tax Report Generation**

## 🎓 Learning Outcomes

This project demonstrates:
- **Financial Data Modeling** best practices
- **Complex Aggregation Queries** with Django ORM
- **Time-based Data Analysis** techniques
- **Data Validation** for financial applications
- **Report Generation** and data export
- **Budget Management** algorithms
- **Real-world Business Logic** implementation

## 💡 Interview Topics Covered

- **Aggregation and Annotations**
- **Date/Time handling in APIs**
- **Financial calculations and precision**
- **Data validation and constraints**
- **Complex filtering and search**
- **Report generation techniques**
- **Performance optimization for analytics**

---

**Perfect for demonstrating financial application development skills!** 💰
