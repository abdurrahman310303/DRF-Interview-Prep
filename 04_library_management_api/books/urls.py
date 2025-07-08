from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import AuthorViewSet, GenreViewSet, BookViewSet
from members.views import MemberViewSet

router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('genres', GenreViewSet)
router.register('books', BookViewSet)
router.register('members', MemberViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
