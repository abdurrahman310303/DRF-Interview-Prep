# User Management System

A comprehensive Django REST Framework API for managing users, profiles, and authentication with role-based access control and JWT authentication.

## Features

### Authentication & Security
- **JWT Authentication** with access and refresh tokens
- **Role-based Access Control** (Admin, Moderator, User)
- **Password Reset** via email
- **Strong Password Validation**
- **Session Management** with token blacklisting

### User Management
- **Custom User Model** with extended fields
- **User Registration & Login**
- **Profile Management** with privacy settings
- **Role Management** (Admin only)
- **User Verification & Activation**
- **Advanced User Search & Filtering**

### Profile System
- **Comprehensive Profile Model** with personal, professional, and preference data
- **Privacy Controls** for profile visibility
- **Social Media Integration**
- **Address Management**
- **Notification Preferences**

### Admin Features
- **Custom Admin Interface** with advanced actions
- **Bulk Operations** (verify, activate, deactivate users)
- **User Statistics & Analytics**
- **Role Assignment & Management**

## Project Structure

```
user_management_system/
├── user_management/          # Main project settings
├── users/                    # User management app
│   ├── models.py            # Custom User model
│   ├── views.py             # User views and ViewSets
│   ├── serializers.py       # User serializers
│   ├── permissions.py       # Custom permissions
│   └── admin.py             # Custom admin interface
├── profiles/                 # Profile management app
│   ├── models.py            # Profile model
│   ├── views.py             # Profile views and ViewSets
│   ├── serializers.py       # Profile serializers
│   └── admin.py             # Profile admin interface
├── authentication/           # Authentication app
│   └── views.py             # Auth views (login, register, password reset)
└── requirements.txt          # Project dependencies
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (JWT)
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/change-password/` - Change password
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset-confirm/` - Confirm password reset
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/` - List users (filtered by role)
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user (admin/moderator)
- `DELETE /api/users/{id}/` - Delete user (admin only)
- `GET /api/users/me/` - Get current user
- `PUT /api/users/{id}/role/` - Update user role (admin only)
- `POST /api/users/{id}/activate/` - Activate user (admin/moderator)
- `POST /api/users/{id}/deactivate/` - Deactivate user (admin/moderator)
- `POST /api/users/{id}/verify/` - Verify user (admin/moderator)
- `GET /api/users/stats/` - User statistics (admin only)

### Profiles
- `GET /api/profiles/` - List profiles (filtered by role)
- `GET /api/profiles/{id}/` - Get profile details
- `PUT /api/profiles/{id}/` - Update profile
- `GET /api/profiles/public/` - List public profiles
- `PUT /api/profiles/{id}/privacy/` - Update privacy settings
- `PUT /api/profiles/{id}/preferences/` - Update preferences

## Key Features Explained

### Role-Based Access Control
- **Admin**: Full access to all users and profiles
- **Moderator**: Can manage regular users and profiles
- **User**: Can only access their own data

### JWT Authentication
- Access tokens expire in 5 minutes
- Refresh tokens expire in 1 day
- Automatic token refresh handling
- Secure logout with token blacklisting

### Profile Privacy
- **Public**: Visible to all users
- **Friends**: Visible to friends only
- **Private**: Visible to owner only
- **Custom**: Granular control over specific fields

### Advanced Filtering
- Search by username, name, email
- Filter by role, status, verification
- Order by various fields
- Pagination support

## Testing with Postman

Import the provided Postman collection to test all endpoints:
- Test user registration and login
- Verify JWT token handling
- Test role-based permissions
- Test profile management
- Test admin operations

## Security Features

- Password strength validation
- JWT token security
- Role-based permissions
- Object-level permissions
- Input validation and sanitization
- CSRF protection
- Secure password reset flow

## Performance Features

- Database query optimization
- Efficient filtering and search
- Pagination for large datasets
- Caching support ready
- Optimized serializers

This project demonstrates advanced Django REST Framework concepts including custom user models, complex permissions, JWT authentication, and comprehensive API design patterns.
