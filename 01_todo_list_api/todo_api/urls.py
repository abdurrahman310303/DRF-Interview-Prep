from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todos.views import TodoViewSet
from users.views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('api/users/logout/', UserLogoutView.as_view(), name='user-logout'),
    path('api/users/profile/', UserProfileView.as_view(), name='user-profile'),
]