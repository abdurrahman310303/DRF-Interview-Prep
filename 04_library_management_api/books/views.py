from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Author, Genre, Book, BookCopy
from .serializers import (
    AuthorSerializer, GenreSerializer, BookSerializer, 
    BookListSerializer, BookCopySerializer
)
from .filters import BookFilter


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
        serializer = BookListSerializer(books, many=True)
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
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related('authors', 'genres', 'copies').all()
    filterset_class = BookFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'isbn', 'description', 'authors__name', 'publisher']
    ordering_fields = ['title', 'publication_date', 'created_at', 'price']
    ordering = ['title']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get only available books"""
        available_books = self.queryset.filter(available_copies__gt=0)
        page = self.paginate_queryset(available_books)
        if page is not None:
            serializer = BookListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BookListSerializer(available_books, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        """Reserve a copy of the book"""
        book = self.get_object()
        if book.reserve_copy():
            return Response({
                'message': 'Book copy reserved successfully',
                'available_copies': book.available_copies
            })
        else:
            return Response(
                {'error': 'No copies available'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search endpoint"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Search query required'}, status=status.HTTP_400_BAD_REQUEST)
        
        books = self.queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(authors__name__icontains=query) |
            Q(genres__name__icontains=query) |
            Q(isbn__icontains=query)
        ).distinct()
        
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)


class BookCopyViewSet(viewsets.ModelViewSet):
    queryset = BookCopy.objects.select_related('book').all()
    serializer_class = BookCopySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['book', 'condition', 'is_available']
    search_fields = ['copy_number', 'location', 'notes']
    ordering_fields = ['copy_number', 'acquired_date']
    ordering = ['book__title', 'copy_number']
