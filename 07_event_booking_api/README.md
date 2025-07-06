# Event Booking API - DRF Interview Prep Project

## 🎯 Project Overview

A comprehensive Django REST Framework API for event booking and management that demonstrates:
- **Booking System Architecture** with seat management
- **Payment Integration** patterns
- **Time-based Availability** management
- **Complex Business Rules** for pricing and cancellation
- **Notification Systems** for event updates
- **Multi-tenant Architecture** for event organizers

## 🚀 Features

### **Event Management**
- Create and manage events (concerts, workshops, conferences)
- Venue management with seating charts
- Multiple ticket types (VIP, Regular, Student, etc.)
- Dynamic pricing based on demand and time
- Event categories and tags
- Recurring event support

### **Booking System**
- Real-time seat availability
- Booking reservation system (temp hold)
- Group bookings and bulk discounts
- Waitlist management for sold-out events
- Booking confirmation and QR codes
- Refund and cancellation management

### **User Management**
- Customer profiles with booking history
- Event organizer accounts
- Loyalty programs and points
- Wishlist and event notifications
- Social login integration

### **Payment Features**
- Multiple payment gateways
- Payment status tracking
- Refund processing
- Discount codes and coupons
- Split payments for group bookings
- Invoice generation

### **Analytics & Reporting**
- Event performance metrics
- Revenue tracking
- Attendance analytics
- Popular events and trending
- Organizer dashboard

## 🏗️ System Architecture

### **Database Models**
- **Event**: Core event information
- **Venue**: Venue details with seating capacity
- **Ticket**: Ticket types and pricing
- **Booking**: Customer bookings
- **Payment**: Payment tracking
- **Seat**: Individual seat management
- **EventOrganizer**: Multi-tenant organizer accounts

## 📁 Project Structure

```
07_event_booking_api/
├── booking_api/              # Main Django project
│   ├── settings.py           # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── events/                   # Event management app
│   ├── models.py            # Event, Venue models
│   ├── serializers.py       # Event serializers
│   ├── views.py             # Event ViewSets
│   ├── filters.py           # Event filters
│   └── admin.py             # Admin interface
├── bookings/                 # Booking management app
│   ├── models.py            # Booking, Ticket models
│   ├── serializers.py       # Booking serializers
│   ├── views.py             # Booking ViewSets
│   ├── utils.py             # Booking logic
│   └── admin.py             # Admin interface
├── payments/                 # Payment processing app
│   ├── models.py            # Payment models
│   ├── serializers.py       # Payment serializers
│   ├── views.py             # Payment ViewSets
│   ├── gateways.py          # Payment gateway integration
│   └── admin.py             # Admin interface
├── users/                    # User management app
│   ├── models.py            # User profile models
│   ├── serializers.py       # User serializers
│   ├── views.py             # User ViewSets
│   └── admin.py             # Admin interface
├── notifications/            # Notification system app
│   ├── models.py            # Notification models
│   ├── views.py             # Notification ViewSets
│   ├── tasks.py             # Celery tasks
│   └── admin.py             # Admin interface
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🛠️ Installation & Setup

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Environment Variables**
Create `.env` file:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### **3. Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **4. Load Sample Data**
```bash
python manage.py loaddata fixtures/venues.json
python manage.py loaddata fixtures/events.json
```

### **5. Start Redis and Celery**
```bash
# Terminal 1 - Redis
redis-server

# Terminal 2 - Celery Worker
celery -A booking_api worker -l info

# Terminal 3 - Celery Beat (for scheduled tasks)
celery -A booking_api beat -l info
```

### **6. Run Development Server**
```bash
python manage.py runserver
```

## 🌐 API Endpoints

### **Events**
- `GET /api/events/` - List events with filtering
- `POST /api/events/` - Create new event (organizers only)
- `GET /api/events/{id}/` - Get event details
- `PUT /api/events/{id}/` - Update event
- `DELETE /api/events/{id}/` - Cancel event
- `GET /api/events/trending/` - Trending events
- `GET /api/events/upcoming/` - Upcoming events
- `POST /api/events/{id}/follow/` - Follow event for updates

### **Venues**
- `GET /api/venues/` - List venues
- `POST /api/venues/` - Add new venue
- `GET /api/venues/{id}/` - Get venue details
- `GET /api/venues/{id}/seating-chart/` - Get seating layout
- `GET /api/venues/{id}/events/` - Events at venue

### **Bookings**
- `GET /api/bookings/` - List user bookings
- `POST /api/bookings/reserve/` - Reserve seats (temporary hold)
- `POST /api/bookings/confirm/` - Confirm reservation
- `GET /api/bookings/{id}/` - Get booking details
- `PUT /api/bookings/{id}/cancel/` - Cancel booking
- `GET /api/bookings/{id}/ticket/` - Download ticket
- `POST /api/bookings/group/` - Group booking

### **Tickets & Availability**
- `GET /api/events/{id}/tickets/` - Available ticket types
- `GET /api/events/{id}/availability/` - Real-time availability
- `POST /api/events/{id}/check-seats/` - Check specific seats
- `GET /api/events/{id}/seating/` - Seating chart with availability

### **Payments**
- `POST /api/payments/create-intent/` - Create payment intent
- `POST /api/payments/confirm/` - Confirm payment
- `GET /api/payments/{id}/status/` - Payment status
- `POST /api/payments/{id}/refund/` - Process refund
- `GET /api/payments/history/` - Payment history

### **User Management**
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update profile
- `GET /api/users/bookings/` - User booking history
- `GET /api/users/wishlist/` - Event wishlist
- `POST /api/users/wishlist/add/` - Add to wishlist
- `GET /api/users/loyalty-points/` - Loyalty points balance

### **Organizer Dashboard**
- `GET /api/organizers/events/` - Organizer's events
- `GET /api/organizers/analytics/` - Event analytics
- `GET /api/organizers/revenue/` - Revenue reports
- `GET /api/organizers/attendees/{event_id}/` - Event attendees
- `POST /api/organizers/bulk-email/` - Send bulk emails

## 📊 Data Models

### **Event Model**
```python
class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey('EventOrganizer', on_delete=models.CASCADE)
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    tags = models.ManyToManyField('Tag')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    is_recurring = models.BooleanField(default=False)
    max_attendees = models.PositiveIntegerField()
    min_age = models.PositiveIntegerField(null=True, blank=True)
    featured_image = models.ImageField(upload_to='events/')
    created_at = models.DateTimeField(auto_now_add=True)
```

### **Booking Model**
```python
class Booking(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),  # Temporary hold
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
    ]
    
    booking_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    tickets = models.ManyToManyField('Ticket', through='BookingTicket')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    payment_status = models.CharField(max_length=20, default='pending')
    special_requests = models.TextField(blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
```

### **Ticket Model**
```python
class Ticket(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # VIP, Regular, Student
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_total = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField(default=0)
    sale_start = models.DateTimeField()
    sale_end = models.DateTimeField()
    is_refundable = models.BooleanField(default=True)
    refund_deadline = models.DateTimeField(null=True, blank=True)
    perks = models.JSONField(default=list)  # List of perks for this ticket
```

## 🧪 Testing the API

### **1. Create Event**
```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tech Conference 2024",
    "description": "Annual technology conference",
    "venue": 1,
    "category": "conference",
    "start_datetime": "2024-06-15T09:00:00Z",
    "end_datetime": "2024-06-15T18:00:00Z",
    "registration_start": "2024-05-01T00:00:00Z",
    "registration_end": "2024-06-14T23:59:59Z",
    "max_attendees": 500,
    "min_age": 18
  }'
```

### **2. Reserve Seats**
```bash
curl -X POST http://localhost:8000/api/bookings/reserve/ \
  -H "Content-Type: application/json" \
  -d '{
    "event": 1,
    "tickets": [
      {"ticket_type": 1, "quantity": 2},
      {"ticket_type": 2, "quantity": 1}
    ],
    "seats": ["A1", "A2", "B1"]
  }'
```

### **3. Confirm Booking**
```bash
curl -X POST http://localhost:8000/api/bookings/confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": "550e8400-e29b-41d4-a716-446655440000",
    "payment_method": "stripe",
    "special_requests": "Wheelchair accessible seating"
  }'
```

## 🔍 Advanced Features

### **Smart Pricing**
- Dynamic pricing based on demand
- Early bird discounts
- Last-minute deals
- Group booking discounts
- Loyalty program benefits

### **Real-time Updates**
- Live seat availability via WebSockets
- Event updates and notifications
- Booking confirmation in real-time
- Payment status updates

### **Advanced Analytics**
- Revenue forecasting
- Attendance patterns
- Popular time slots
- Geographic analysis
- Marketing campaign effectiveness

## 🔐 Business Rules

### **Booking Rules**
- Maximum 6 tickets per transaction
- Seat reservation holds for 15 minutes
- Refunds allowed up to 24 hours before event
- Group discounts for 10+ tickets
- VIP ticket holders get priority booking

### **Payment Rules**
- Multiple payment methods supported
- Split payments for group bookings
- Automatic refund processing
- Payment failure retry mechanism
- Currency conversion support

### **Event Rules**
- Events can be cancelled up to 48 hours before
- Minimum 50% attendance required for break-even
- Automatic waitlist activation when sold out
- Age verification for restricted events

## 🚀 Next Steps & Enhancements

### **Immediate Improvements**
1. **Mobile App** with QR code scanning
2. **Social Media Integration** for event sharing
3. **Advanced Analytics Dashboard**
4. **Multi-language Support**

### **Advanced Features**
1. **AI-powered Event Recommendations**
2. **Blockchain-based Ticket Verification**
3. **AR/VR Event Previews**
4. **Integration with Calendar Apps**
5. **Live Streaming Integration**

## 🎓 Learning Outcomes

This project demonstrates:
- **Complex Booking System** architecture
- **Real-time Data Management** with WebSockets
- **Payment Gateway Integration** patterns
- **Multi-tenant Application** design
- **Time-based Business Logic** implementation
- **Notification System** architecture
- **Analytics and Reporting** features
- **State Management** for booking workflows

## 💡 Interview Topics Covered

- **Concurrency handling** in booking systems
- **Payment processing** and financial transactions
- **Real-time features** with WebSockets
- **Complex business rules** implementation
- **Multi-tenant architecture** patterns
- **Performance optimization** for high-traffic scenarios
- **Data consistency** in distributed systems
- **Event-driven architecture** principles

---

**Perfect for demonstrating complex booking system and payment integration skills!** 🎫
