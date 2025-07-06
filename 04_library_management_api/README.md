# Library Management System API

A comprehensive Django REST Framework API for managing library operations including book catalog, member management, and borrowing system.

## Features

- **Book Management**: CRUD operations for books with author and genre relationships
- **Member Management**: Library member registration with different membership tiers  
- **Borrowing System**: Book checkout/return with due dates and fine calculations
- **Inventory Tracking**: Real-time book availability and reservation system

## Tech Stack

- Django REST Framework
- PostgreSQL/SQLite
- JWT Authentication
- Django Filters for advanced filtering
- Pillow for image handling

## Installation

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API Endpoints

- `/api/books/` - Book management
- `/api/authors/` - Author management  
- `/api/members/` - Member management
- `/api/borrowing/` - Borrowing operations

## Learning Focus

- Complex model relationships (Many-to-Many, Foreign Keys)
- Business logic implementation (fines, borrowing limits)
- Inventory management patterns
- Automated business processes
