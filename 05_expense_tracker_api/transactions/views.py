from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer, TransactionSummarySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'category', 'is_recurring']
    search_fields = ['description', 'notes', 'category__name']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).select_related('category')
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get transaction summary for the current month"""
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        
        queryset = self.get_queryset().filter(date__gte=start_of_month)
        
        income_total = queryset.filter(type='income').aggregate(
            total=Sum('amount'))['total'] or 0
        expense_total = queryset.filter(type='expense').aggregate(
            total=Sum('amount'))['total'] or 0
        
        summary_data = {
            'total_income': income_total,
            'total_expenses': expense_total,
            'net_amount': income_total - expense_total,
            'transaction_count': queryset.count(),
            'period': f"{start_of_month.strftime('%B %Y')}"
        }
        
        serializer = TransactionSummarySerializer(summary_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get transactions grouped by category"""
        queryset = self.get_queryset()
        
        # Get query parameters for date filtering
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        category_summary = queryset.values('category__name', 'type').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('category__name')
        
        return Response(category_summary)
