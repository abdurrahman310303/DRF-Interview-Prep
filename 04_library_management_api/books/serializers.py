from rest_framework import serializers
from .models import Author, Genre, Book


class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(source='books.count', read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'birth_date', 'nationality', 
                 'created_at', 'books_count']
        read_only_fields = ['created_at']


class GenreSerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(source='books.count', read_only=True)
    
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'created_at', 'books_count']
        read_only_fields = ['created_at']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    author_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True,
        required=False
    )
    genre_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True,
        required=False
    )
    availability_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'authors', 'genres', 'author_ids', 
            'genre_ids', 'publication_date', 'publisher', 'description', 
            'pages', 'language', 'total_copies', 'available_copies', 
            'price', 'cover_image', 'created_at', 'updated_at',
            'availability_status', 'is_available'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_available']
    
    def get_availability_status(self, obj):
        if obj.available_copies == 0:
            return "Out of Stock"
        elif obj.available_copies <= 2:
            return "Limited Stock"
        else:
            return "Available"
    
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
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update relationships
        if author_ids is not None:
            instance.authors.set(author_ids)
        if genre_ids is not None:
            instance.genres.set(genre_ids)
            
        return instance


class BookSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing books"""
    authors_names = serializers.StringRelatedField(source='authors', many=True)
    genres_names = serializers.StringRelatedField(source='genres', many=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'authors_names', 'genres_names',
            'publication_date', 'available_copies', 'price', 'is_available'
        ]
