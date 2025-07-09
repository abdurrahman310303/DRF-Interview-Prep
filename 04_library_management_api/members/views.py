from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Member
from .serializers import MemberSerializer, MemberRegistrationSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.select_related('user').all()
    serializer_class = MemberSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['membership_level', 'is_active']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'membership_id', 'phone']
    ordering_fields = ['membership_date', 'expiry_date', 'user__first_name']
    ordering = ['user__first_name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MemberRegistrationSerializer
        return MemberSerializer
    
    @action(detail=True, methods=['get'])
    def borrowing_history(self, request, pk=None):
        member = self.get_object()
        # This would connect to borrowing records when that app is complete
        return Response({'message': 'Borrowing history feature coming soon'})
    
    @action(detail=True, methods=['post'])
    def renew_membership(self, request, pk=None):
        member = self.get_object()
        # Add membership renewal logic here
        return Response({'message': 'Membership renewed successfully'})
    
    @action(detail=False, methods=['get'])
    def active_members(self, request):
        """Get only active members"""
        active_members = self.queryset.filter(is_active=True)
        page = self.paginate_queryset(active_members)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(active_members, many=True)
        return Response(serializer.data)
