from django.contrib import admin
from .models import Author, Genre, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'birth_date', 'created_at']
    list_filter = ['nationality', 'birth_date']
    search_fields = ['name', 'biography']
    ordering = ['name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'publisher', 'publication_date', 'total_copies', 'available_copies']
    list_filter = ['publication_date', 'language', 'genres', 'authors']
    search_fields = ['title', 'isbn', 'description', 'publisher']
    filter_horizontal = ['authors', 'genres']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'isbn', 'authors', 'genres')
        }),
        ('Publication Details', {
            'fields': ('publisher', 'publication_date', 'pages', 'language')
        }),
        ('Content', {
            'fields': ('description', 'cover_image')
        }),
        ('Inventory', {
            'fields': ('total_copies', 'available_copies', 'price')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
