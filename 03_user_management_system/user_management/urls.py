from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from profiles.views import ProfileViewSet

# Create routers for ViewSets
user_router = DefaultRouter()
user_router.register(r'users', UserViewSet, basename='user')

profile_router = DefaultRouter()
profile_router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include(user_router.urls)),
    path('api/', include(profile_router.urls)),
    
    # Authentication endpoints
    path('api/auth/', include('authentication.urls')),
    
    # User-specific endpoints
    path('api/users/me/', UserViewSet.as_view({'get': 'me'}), name='user-me'),
    path('api/users/stats/', UserViewSet.as_view({'get': 'stats'}), name='user-stats'),
    
    # Profile-specific endpoints
    path('api/profiles/public/', ProfileViewSet.as_view({'get': 'public'}), name='profile-public'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
