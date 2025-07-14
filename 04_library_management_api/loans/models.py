from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from members.models import Member
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class BookLoan(models.Model):
    LOAN_STATUS_CHOICES = [
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default='active')
    renewal_count = models.PositiveIntegerField(default=0)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-loan_date']
        unique_together = ['member', 'book', 'loan_date']
    
    def __str__(self):
        return f"{self.member} - {self.book.title}"
    
    @property
    def is_overdue(self):
        return timezone.now() > self.due_date and self.status == 'active'
    
    @property
    def days_overdue(self):
        if self.is_overdue:
            return (timezone.now() - self.due_date).days
        return 0
    
    def calculate_fine(self):
        if self.is_overdue:
            # $1 per day overdue
            fine = Decimal('1.00') * self.days_overdue
            return fine
        return Decimal('0.00')
    
    def save(self, *args, **kwargs):
        # Set due date if not provided (14 days from loan date)
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)
        
        # Update fine amount for overdue books
        if self.status == 'overdue':
            self.fine_amount = self.calculate_fine()
        
        super().save(*args, **kwargs)


class Reservation(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reservations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-reservation_date']
        unique_together = ['member', 'book']
    
    def __str__(self):
        return f"{self.member} reserved {self.book.title}"
    
    def save(self, *args, **kwargs):
        # Set expiry date (3 days to pick up reserved book)
        if not self.expiry_date:
            self.expiry_date = timezone.now() + timedelta(days=3)
        super().save(*args, **kwargs)
