from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Venue, EventCategory, TicketType, Booking, Payment, EventReview


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'address', 'city', 'capacity', 'description', 
                 'image', 'amenities', 'created_at']


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'description']


class TicketTypeSerializer(serializers.ModelSerializer):
    remaining_tickets = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = TicketType
        fields = [
            'id', 'name', 'description', 'price', 'quantity_available',
            'quantity_sold', 'sale_start_datetime', 'sale_end_datetime',
            'is_active', 'remaining_tickets', 'is_available'
        ]


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)
    venue = VenueSerializer(read_only=True)
    category = EventCategorySerializer(read_only=True)
    ticket_types = TicketTypeSerializer(many=True, read_only=True)
    venue_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True)
    is_sold_out = serializers.ReadOnlyField()
    available_seats = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'organizer', 'category', 'category_id',
            'venue', 'venue_id', 'start_datetime', 'end_datetime', 'max_attendees',
            'current_attendees', 'base_price', 'image', 'status', 'is_free',
            'requires_approval', 'tags', 'ticket_types', 'is_sold_out',
            'available_seats', 'created_at', 'updated_at'
        ]
        read_only_fields = ['organizer', 'current_attendees', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)


class EventSummarySerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_sold_out = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'organizer_name', 'venue_name', 'category_name',
            'start_datetime', 'end_datetime', 'base_price', 'image', 'status',
            'is_free', 'max_attendees', 'current_attendees', 'is_sold_out'
        ]


class BookingSerializer(serializers.ModelSerializer):
    event = EventSummarySerializer(read_only=True)
    ticket_type = TicketTypeSerializer(read_only=True)
    event_id = serializers.IntegerField(write_only=True)
    ticket_type_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_id', 'user', 'event', 'event_id', 'ticket_type',
            'ticket_type_id', 'quantity', 'total_amount', 'status',
            'booking_datetime', 'confirmation_datetime', 'special_requests'
        ]
        read_only_fields = ['user', 'booking_id', 'total_amount', 'booking_datetime']
    
    def validate(self, data):
        ticket_type_id = data.get('ticket_type_id')
        quantity = data.get('quantity', 1)
        
        if ticket_type_id:
            ticket_type = TicketType.objects.get(id=ticket_type_id)
            
            # Check availability
            if not ticket_type.is_available:
                raise serializers.ValidationError("This ticket type is not available")
            
            # Check quantity
            if quantity > ticket_type.remaining_tickets:
                raise serializers.ValidationError(
                    f"Only {ticket_type.remaining_tickets} tickets available"
                )
        
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        booking = super().create(validated_data)
        
        # Update ticket type sold quantity
        booking.ticket_type.quantity_sold += booking.quantity
        booking.ticket_type.save()
        
        # Update event current attendees
        booking.event.current_attendees += booking.quantity
        booking.event.save()
        
        return booking


class PaymentSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'booking', 'amount', 'payment_method', 'transaction_id',
            'status', 'payment_datetime', 'failure_reason', 'created_at'
        ]
        read_only_fields = ['transaction_id', 'created_at']


class EventReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = EventReview
        fields = ['id', 'event', 'reviewer', 'rating', 'comment', 'created_at']
        read_only_fields = ['reviewer', 'created_at']
    
    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)
