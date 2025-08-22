# User Management System - Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Step-by-Step Setup

### 1. Create Virtual Environment
```bash
# Navigate to the project directory
cd 03_user_management_system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Note**: For Gmail, you'll need to:
1. Enable 2-factor authentication
2. Generate an "App Password" in your Google Account settings
3. Use that app password instead of your regular password

### 4. Database Setup
```bash
# Make migrations
python manage.py makemigrations users
python manage.py makemigrations profiles
python manage.py makemigrations authentication

# Apply migrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
# Follow the prompts to create an admin user
# Username: admin
# Email: admin@example.com
# Password: (create a strong password)
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The API will be available at: http://localhost:8000/

## Testing the API

### 1. Import Postman Collection
- Open Postman
- Import the `User_Management_System.postman_collection.json` file
- Set the `base_url` variable to `http://localhost:8000`

### 2. Test Authentication Flow
1. **Register a new user** using `POST /api/auth/register/`
2. **Login** using `POST /api/auth/login/` (this will automatically save your tokens)
3. **Test protected endpoints** using the saved access token

### 3. Test Admin Operations
1. **Login as admin** using the superuser credentials
2. **Test admin-only endpoints** like user management and statistics

## API Endpoints Overview

### Public Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/profiles/public/` - List public profiles

### Protected Endpoints (Require Authentication)
- `GET /api/users/me/` - Get current user
- `PUT /api/profiles/{id}/` - Update profile
- `POST /api/auth/logout/` - User logout

### Admin-Only Endpoints
- `GET /api/users/stats/` - User statistics
- `PUT /api/users/{id}/role/` - Update user role
- `POST /api/users/{id}/activate/` - Activate user

## Common Issues and Solutions

### 1. Migration Errors
If you get migration errors:
```bash
# Reset migrations (WARNING: This will delete your database)
rm -rf */migrations/
python manage.py makemigrations
python manage.py migrate
```

### 2. JWT Token Issues
- Ensure `djangorestframework-simplejwt` is installed
- Check that JWT settings are properly configured in `settings.py`
- Verify token expiration times

### 3. Email Configuration Issues
- Ensure SMTP settings are correct
- Check that app passwords are generated for Gmail
- Test email functionality with a simple email first

### 4. Permission Errors
- Verify user roles are properly set
- Check that custom permissions are working
- Ensure admin user has the correct role

## Development Workflow

### 1. Making Changes
1. Make changes to models, views, or serializers
2. Create and apply migrations if needed
3. Test endpoints with Postman
4. Check admin interface functionality

### 2. Adding New Features
1. Create new models in appropriate apps
2. Add serializers for new models
3. Create views and ViewSets
4. Add URL patterns
5. Update permissions if needed
6. Test thoroughly

### 3. Debugging
- Use Django shell: `python manage.py shell`
- Check Django logs in console
- Use Postman's console for API debugging
- Verify database state in admin interface

## Production Considerations

### 1. Security
- Change `DEBUG=False` in production
- Use strong, unique `SECRET_KEY`
- Configure proper CORS settings
- Use HTTPS in production
- Set appropriate JWT token expiration times

### 2. Database
- Use PostgreSQL or MySQL in production
- Configure database connection pooling
- Set up database backups

### 3. Email
- Use production email service (SendGrid, AWS SES, etc.)
- Configure proper email templates
- Set up email monitoring

## Next Steps

After setting up the basic system:
1. **Add more features**: User groups, permissions, audit logs
2. **Implement caching**: Redis for session storage and caching
3. **Add monitoring**: Logging, metrics, health checks
4. **Create tests**: Unit tests, integration tests
5. **Documentation**: API documentation with tools like drf-spectacular

## Support

If you encounter issues:
1. Check the Django error logs
2. Verify all dependencies are installed
3. Ensure database migrations are applied
4. Check environment variables are set correctly
5. Verify JWT configuration in settings

Happy coding! 🚀
