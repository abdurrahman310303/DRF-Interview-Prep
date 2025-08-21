# Simple Blog API - DRF Interview Prep Project

## 🎯 Project Overview

A complete Django REST Framework blog API that demonstrates advanced DRF concepts including:
- **Model Relationships** (One-to-Many, Many-to-Many)
- **Nested Serializers** with complex data structures
- **Custom Permissions** for secure access control
- **Advanced Filtering and Search** capabilities
- **File Uploads** for images and media
- **ViewSets and Routers** for efficient CRUD operations

## 🚀 Features

### **User Management**
- User registration and authentication
- Custom user model with profile fields
- Session-based authentication
- User profile management

### **Blog Posts**
- Create, read, update, delete blog posts
- Draft and published post status
- Rich content with excerpts
- Featured images support
- Author-only editing permissions

### **Categories**
- Many-to-many relationship with posts
- Automatic slug generation
- Category management

### **Comments**
- Comment system for posts
- Approval workflow
- Author-only editing

### **Advanced Features**
- Full-text search across posts
- Advanced filtering by status, author, categories
- Pagination and ordering
- Custom actions (publish, like)

## 🏗️ System Architecture

### **Database Models**
- **User**: Custom user model with bio and profile picture
- **Category**: Blog post categories with slugs
- **Post**: Blog posts with rich content and metadata
- **Comment**: User comments on posts

### **API Design**
- RESTful endpoints following DRF conventions
- Proper HTTP status codes
- JSON request/response format
- Consistent error handling

## 📁 Project Structure

```
02_simple_blog_api/
├── blog_api/                 # Main Django project
│   ├── __init__.py
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── users/                    # User management app
│   ├── models.py            # Custom User model
│   ├── serializers.py       # User data validation
│   ├── views.py             # Authentication views
│   └── admin.py             # Admin interface
├── categories/               # Category management app
│   ├── models.py            # Category model
│   ├── serializers.py       # Category serializers
│   ├── views.py             # Category ViewSet
│   └── admin.py             # Admin interface
├── posts/                    # Blog posts app
│   ├── models.py            # Post and Comment models
│   ├── serializers.py       # Post serializers
│   ├── views.py             # Post ViewSet
│   ├── permissions.py       # Custom permissions
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

### **3. Create Superuser**
```bash
python manage.py createsuperuser
```

### **4. Run Development Server**
```bash
python manage.py runserver
```

## 🌐 API Endpoints

### **User Management**
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/logout/` - User logout
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update user profile
- `GET /api/users/` - List all users

### **Categories**
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create new category
- `GET /api/categories/{slug}/` - Get specific category
- `PUT /api/categories/{slug}/` - Update category
- `DELETE /api/categories/{slug}/` - Delete category

### **Blog Posts**
- `GET /api/posts/` - List all posts (paginated)
- `POST /api/posts/` - Create new post
- `GET /api/posts/{slug}/` - Get specific post
- `PUT /api/posts/{slug}/` - Update post
- `DELETE /api/posts/{slug}/` - Delete post
- `POST /api/posts/{slug}/publish/` - Publish draft post
- `POST /api/posts/{slug}/like/` - Like a post

### **Comments**
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create new comment
- `GET /api/comments/{id}/` - Get specific comment
- `PUT /api/comments/{id}/` - Update comment
- `DELETE /api/comments/{id}/` - Delete comment

### **Search**
- `GET /api/search/?q=query` - Search posts by content
- `GET /api/search/?category=slug` - Filter by category
- `GET /api/search/?author=username` - Filter by author

## 🔐 Authentication & Permissions

### **Authentication**
- Session-based authentication
- Login required for most operations
- Public read access to published posts

### **Permissions**
- **Users**: Can only edit their own profile
- **Posts**: Authors can only edit their own posts
- **Comments**: Authors can only edit their own comments
- **Categories**: Read-only for regular users

## 📊 Data Models

### **User Model**
```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, max_length=500)
    profile_picture = models.ImageField(upload_to='profile_pics/')
```

### **Category Model**
```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **Post Model**
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    status = models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')])
    featured_image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
```

### **Comment Model**
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
```

## 🧪 Testing the API

### **1. User Registration**
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "bio": "A test user for the blog API"
  }'
```

### **2. User Login**
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### **3. Create Category**
```bash
curl -X POST http://localhost:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Technology",
    "description": "Technology-related blog posts"
  }'
```

### **4. Create Blog Post**
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started with Django REST Framework",
    "content": "Django REST Framework is a powerful toolkit for building Web APIs...",
    "excerpt": "Learn the basics of building APIs with Django REST Framework",
    "status": "draft",
    "categories": [1]
  }'
```

## 🔍 Advanced Features

### **Filtering**
- Filter posts by status: `?status=published`
- Filter by author: `?author=username`
- Filter by category: `?categories=1`

### **Search**
- Search by content: `?search=django`
- Search by title: `?search=getting started`

### **Ordering**
- Order by date: `?ordering=-created_at`
- Order by title: `?ordering=title`
- Order by views: `?ordering=-views_count`

### **Pagination**
- Default: 10 items per page
- Navigate pages: `?page=2`

## 🚀 Next Steps & Enhancements

### **Immediate Improvements**
1. **Add comprehensive tests** for all endpoints
2. **Implement JWT authentication** for better security
3. **Add rate limiting** to prevent abuse
4. **Create API documentation** with drf-spectacular

### **Advanced Features**
1. **Redis caching** for frequently accessed data
2. **Background tasks** with Celery for image processing
3. **Real-time notifications** with WebSockets
4. **Advanced search** with Elasticsearch
5. **Social features** like following users and liking posts

## 🎓 Learning Outcomes

This project demonstrates:
- **Advanced DRF concepts** beyond basic CRUD
- **Complex model relationships** and nested serializers
- **Custom permissions** and security best practices
- **API design patterns** for scalable applications
- **File handling** and media management
- **Search and filtering** implementation

## 📚 Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Django Models Documentation](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [DRF ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)

---

**Ready to test your Blog API? Use the Postman collection below to explore all the endpoints!** 🚀
