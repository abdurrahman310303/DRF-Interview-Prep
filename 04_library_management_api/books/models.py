from django.db import models
from django.core.validators import RegexValidator


class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    isbn_validator = RegexValidator(
        regex=r'^\d{13}$',
        message='ISBN must be exactly 13 digits'
    )
    
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True, validators=[isbn_validator])
    authors = models.ManyToManyField(Author, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')
    publication_date = models.DateField()
    publisher = models.CharField(max_length=200)
    description = models.TextField()
    pages = models.PositiveIntegerField()
    language = models.CharField(max_length=50, default='English')
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['title']
        
    def __str__(self):
        return self.title
    
    @property
    def is_available(self):
        return self.available_copies > 0
    
    def reserve_copy(self):
        if self.available_copies > 0:
            self.available_copies -= 1
            self.save()
            return True
        return False
    
    def return_copy(self):
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            self.save()


class BookCopy(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('damaged', 'Damaged'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
    copy_number = models.CharField(max_length=50)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    location = models.CharField(max_length=100, help_text='Shelf location')
    is_available = models.BooleanField(default=True)
    acquired_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['book', 'copy_number']
        ordering = ['book', 'copy_number']
    
    def __str__(self):
        return f"{self.book.title} - Copy {self.copy_number}"
