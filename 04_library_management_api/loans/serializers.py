from rest_framework import serializers
from .models import BookLoan, Reservation
from books.serializers import BookSummarySerializer
from members.serializers import MemberSerializer


class BookLoanSerializer(serializers.ModelSerializer):
    book = BookSummarySerializer(read_only=True)
    member = MemberSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    member_id = serializers.IntegerField(write_only=True)
    is_overdue = serializers.ReadOnlyField()
    days_overdue = serializers.ReadOnlyField()
    calculated_fine = serializers.SerializerMethodField()
    
    class Meta:
        model = BookLoan
        fields = [
            'id', 'book', 'member', 'book_id', 'member_id', 'loan_date',
            'due_date', 'return_date', 'status', 'renewal_count', 'fine_amount',
            'notes', 'is_overdue', 'days_overdue', 'calculated_fine',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['loan_date', 'created_at', 'updated_at']
    
    def get_calculated_fine(self, obj):
        return str(obj.calculate_fine())
    
    def validate(self, data):
        # Check if member has reached borrowing limit
        member_id = data.get('member_id')
        if member_id:
            from members.models import Member
            member = Member.objects.get(id=member_id)
            active_loans = BookLoan.objects.filter(
                member=member, 
                status='active'
            ).count()
            
            if active_loans >= member.borrowing_limit:
                raise serializers.ValidationError(
                    f"Member has reached borrowing limit of {member.borrowing_limit} books"
                )
        
        # Check book availability
        book_id = data.get('book_id')
        if book_id:
            from books.models import Book
            book = Book.objects.get(id=book_id)
            if book.available_copies <= 0:
                raise serializers.ValidationError("Book is not available for loan")
        
        return data
    
    def create(self, validated_data):
        # Decrease available copies when creating loan
        book_id = validated_data['book_id']
        from books.models import Book
        book = Book.objects.get(id=book_id)
        book.available_copies -= 1
        book.save()
        
        return super().create(validated_data)


class ReservationSerializer(serializers.ModelSerializer):
    book = BookSummarySerializer(read_only=True)
    member = MemberSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    member_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'book', 'member', 'book_id', 'member_id',
            'reservation_date', 'expiry_date', 'is_active', 'notified',
            'created_at'
        ]
        read_only_fields = ['reservation_date', 'created_at']
    
    def validate(self, data):
        # Check if book is available for reservation
        book_id = data.get('book_id')
        member_id = data.get('member_id')
        
        if book_id and member_id:
            # Check if member already has this book on loan
            existing_loan = BookLoan.objects.filter(
                book_id=book_id,
                member_id=member_id,
                status='active'
            ).exists()
            
            if existing_loan:
                raise serializers.ValidationError(
                    "Member already has this book on loan"
                )
            
            # Check if member already has reservation for this book
            existing_reservation = Reservation.objects.filter(
                book_id=book_id,
                member_id=member_id,
                is_active=True
            ).exists()
            
            if existing_reservation:
                raise serializers.ValidationError(
                    "Member already has an active reservation for this book"
                )
        
        return data


class LoanSummarySerializer(serializers.Serializer):
    total_loans = serializers.IntegerField()
    active_loans = serializers.IntegerField()
    overdue_loans = serializers.IntegerField()
    returned_loans = serializers.IntegerField()
    total_fines = serializers.DecimalField(max_digits=10, decimal_places=2)
