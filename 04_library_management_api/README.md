# Library Management API - DRF Interview Prep Project

## 🎯 Project Overview

A comprehensive Django REST Framework API for managing a library system that demonstrates:
- **Complex Model Relationships** (One-to-One, One-to-Many, Many-to-Many)
- **Advanced Filtering and Search** with date ranges
- **Business Logic Implementation** (borrowing, returning, fines)
- **Custom ViewSets and Actions**
- **Inventory Management Patterns**
- **Automated Business Rules**

## 🚀 Features

### **Book Management**
- Book catalog with detailed information
- Author and genre relationships
- ISBN validation
- Availability tracking
- Search by title, author, ISBN, genre

### **Member Management** 
- Library member registration
- Membership levels (Basic, Premium, VIP)
- Member activity tracking
- Borrowing history

### **Borrowing System**
- Book checkout and return
- Due date management
- Fine calculation for overdue books
- Borrowing limits based on membership level
- Renewal system

### **Inventory Features**
- Book availability tracking
- Copy management (multiple copies per book)
- Reservation system
- Stock alerts for low inventory

## 🏗️ System Architecture

### **Database Models**
- **Author**: Author information with biography
- **Genre**: Book categories
- **Book**: Book details with relationships to authors and genres
- **BookCopy**: Individual copies of books for tracking
- **Member**: Library members with membership levels
- **BorrowRecord**: Tracking borrowed books
- **Fine**: Fine management for overdue books

## 📁 Project Structure

```
04_library_management_api/
├── library_api/              # Main Django project
│   ├── settings.py           # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── books/                    # Book management app
│   ├── models.py            # Book, Author, Genre models
│   ├── serializers.py       # Book-related serializers
│   ├── views.py             # Book ViewSets
│   └── admin.py             # Admin interface
├── members/                  # Member management app
│   ├── models.py            # Member model
│   ├── serializers.py       # Member serializers
│   ├── views.py             # Member ViewSet
│   └── admin.py             # Admin interface
├── borrowing/                # Borrowing system app
│   ├── models.py            # BorrowRecord, Fine models
│   ├── serializers.py       # Borrowing serializers
│   ├── views.py             # Borrowing ViewSet
│   ├── utils.py             # Business logic utilities
│   └── admin.py             # Admin interface
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
python manage.py loaddata fixtures/sample_data.json
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

### **Books**
- `GET /api/books/` - List all books with filtering
- `POST /api/books/` - Add new book
- `GET /api/books/{id}/` - Get book details
- `PUT /api/books/{id}/` - Update book
- `DELETE /api/books/{id}/` - Delete book
- `GET /api/books/search/?q=query` - Search books
- `GET /api/books/available/` - List available books
- `POST /api/books/{id}/reserve/` - Reserve a book

### **Authors**
- `GET /api/authors/` - List all authors
- `POST /api/authors/` - Add new author
- `GET /api/authors/{id}/` - Get author details
- `GET /api/authors/{id}/books/` - Get author's books

### **Genres**
- `GET /api/genres/` - List all genres
- `POST /api/genres/` - Add new genre
- `GET /api/genres/{id}/books/` - Get books by genre

### **Members**
- `GET /api/members/` - List all members
- `POST /api/members/` - Register new member
- `GET /api/members/{id}/` - Get member details
- `PUT /api/members/{id}/` - Update member
- `GET /api/members/{id}/history/` - Get borrowing history
- `GET /api/members/{id}/fines/` - Get member's fines

### **Borrowing**
- `GET /api/borrowing/` - List all borrow records
- `POST /api/borrowing/borrow/` - Borrow a book
- `POST /api/borrowing/return/` - Return a book
- `POST /api/borrowing/renew/` - Renew a borrowed book
- `GET /api/borrowing/overdue/` - List overdue books
- `GET /api/borrowing/due-today/` - Books due today

## 🔐 Business Rules

### **Borrowing Limits**
- **Basic Member**: 3 books max
- **Premium Member**: 5 books max  
- **VIP Member**: 10 books max

### **Loan Periods**
- **Basic Member**: 14 days
- **Premium Member**: 21 days
- **VIP Member**: 30 days

### **Fine System**
- ₹2 per day for overdue books
- No new borrowing with outstanding fines > ₹100
- Fine waiver for VIP members (first offense)

## 📊 Data Models

### **Book Model**
```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    description = models.TextField()
    authors = models.ManyToManyField('Author')
    genres = models.ManyToManyField('Genre')
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

### **Member Model**
```python
class Member(models.Model):
    MEMBERSHIP_LEVELS = [
        ('basic', 'Basic'),
        ('premium', 'Premium'), 
        ('vip', 'VIP'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_level = models.CharField(max_length=10, choices=MEMBERSHIP_LEVELS)
    membership_date = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
```

### **BorrowRecord Model**
```python
class BorrowRecord(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book_copy = models.ForeignKey('BookCopy', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    renewed_count = models.PositiveIntegerField(default=0)
    is_returned = models.BooleanField(default=False)
```

## 🧪 Testing the API

### **1. Register Member**
```bash
curl -X POST http://localhost:8000/api/members/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "membership_level": "basic",
    "phone": "9876543210",
    "address": "123 Main St, City"
  }'
```

### **2. Add Book**
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Programming",
    "isbn": "9781234567890",
    "publication_date": "2023-01-15",
    "description": "Complete guide to Python programming",
    "authors": [1],
    "genres": [1, 2],
    "total_copies": 3,
    "available_copies": 3,
    "price": "599.00"
  }'
```

### **3. Borrow Book**
```bash
curl -X POST http://localhost:8000/api/borrowing/borrow/ \
  -H "Content-Type: application/json" \
  -d '{
    "member_id": 1,
    "book_id": 1
  }'
```

## 🔍 Advanced Features

### **Smart Search**
- Search across title, author, ISBN, description
- Filter by genre, availability, publication year
- Sort by popularity, publication date, title

### **Automated Processes**
- Daily fine calculation task
- Overdue book notifications
- Low stock alerts
- Automatic fine calculation on return

### **Reporting**
- Member activity reports
- Popular books tracking
- Fine collection reports
- Inventory status reports

## 🚀 Next Steps & Enhancements

### **Immediate Improvements**
1. **Email Notifications** for due dates and fines
2. **Comprehensive Testing Suite**
3. **API Documentation** with drf-spectacular
4. **Advanced Reporting Dashboard**

### **Advanced Features**
1. **Book Recommendations** based on borrowing history
2. **Digital Library** with e-book support
3. **Mobile App API** with QR code scanning
4. **Integration with External Book APIs**
5. **Advanced Analytics** with reading patterns

## 🎓 Learning Outcomes

This project demonstrates:
- **Complex Business Logic** implementation
- **Advanced Model Relationships** and constraints
- **Custom Actions** and business operations
- **Date/Time Management** in applications
- **Inventory Management Patterns**
- **Financial Calculations** (fines, pricing)
- **Automated Business Processes**

---

**Perfect for learning advanced DRF concepts with real-world business logic!** 📚
