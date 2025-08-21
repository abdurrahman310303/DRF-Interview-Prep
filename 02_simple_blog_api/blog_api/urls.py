"""
URL configuration for blog_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from posts.views import PostViewSet, CommentViewSet, PostSearchView
from categories.views import CategoryViewSet
from users.views import (
    UserRegistrationView, 
    UserLoginView, 
    UserLogoutView, 
    UserProfileView,
    UserListView
)

# Create routers
post_router = DefaultRouter()
post_router.register(r'posts', PostViewSet, basename='post')

comment_router = DefaultRouter()
comment_router.register(r'comments', CommentViewSet, basename='comment')

category_router = DefaultRouter()
category_router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include(post_router.urls)),
    path('api/', include(comment_router.urls)),
    path('api/', include(category_router.urls)),
    
    # User management
    path('api/users/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/users/login/', UserLoginView.as_view(), name='user-login'),
    path('api/users/logout/', UserLogoutView.as_view(), name='user-logout'),
    path('api/users/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    
    # Search
    path('api/search/', PostSearchView.as_view(), name='post-search'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
