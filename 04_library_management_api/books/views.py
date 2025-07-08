from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Author, Genre, Book
from .serializers import AuthorSerializer, GenreSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'biography', 'nationality']
    ordering_fields = ['name', 'birth_date', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        author = self.get_object()
        books = author.books.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        genre = self.get_object()
        books = genre.books.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related('authors', 'genres').all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'isbn', 'description', 'authors__name', 'publisher']
    filterset_fields = ['authors', 'genres', 'language', 'publication_date']
    ordering_fields = ['title', 'publication_date', 'created_at', 'price']
    ordering = ['title']
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get only available books"""
        available_books = self.queryset.filter(available_copies__gt=0)
        page = self.paginate_queryset(available_books)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        """Reserve a copy of the book"""
        book = self.get_object()
        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()
            return Response({
                'message': 'Book copy reserved successfully',
                'available_copies': book.available_copies
            })
        else:
            return Response(
                {'error': 'No copies available'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
