from rest_framework import serializers
from .models import Author, Genre, Book, BookCopy


class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'birth_date', 'nationality', 'books_count', 'created_at']
        
    def get_books_count(self, obj):
        return obj.books.count()


class GenreSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'books_count', 'created_at']
        
    def get_books_count(self, obj):
        return obj.books.count()


class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ['id', 'copy_number', 'condition', 'location', 'is_available', 'acquired_date', 'notes']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    copies = BookCopySerializer(many=True, read_only=True)
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'authors', 'author_ids', 'genres', 'genre_ids',
            'publication_date', 'publisher', 'description', 'pages', 'language',
            'total_copies', 'available_copies', 'is_available', 'price', 
            'cover_image', 'copies', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        author_ids = validated_data.pop('author_ids', [])
        genre_ids = validated_data.pop('genre_ids', [])
        
        book = Book.objects.create(**validated_data)
        
        if author_ids:
            book.authors.set(author_ids)
        if genre_ids:
            book.genres.set(genre_ids)
            
        return book
    
    def update(self, instance, validated_data):
        author_ids = validated_data.pop('author_ids', None)
        genre_ids = validated_data.pop('genre_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if author_ids is not None:
            instance.authors.set(author_ids)
        if genre_ids is not None:
            instance.genres.set(genre_ids)
            
        return instance


class BookListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    authors = serializers.StringRelatedField(many=True, read_only=True)
    genres = serializers.StringRelatedField(many=True, read_only=True)
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'authors', 'genres', 'publication_date',
            'available_copies', 'total_copies', 'is_available', 'price', 'cover_image'
        ]
