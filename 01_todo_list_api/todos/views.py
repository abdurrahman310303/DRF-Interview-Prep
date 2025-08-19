from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Todo
from .serializers import TodoSerializer, TodoToggleSerializer
from .permissions import IsOwnerOrReadOnly

class TodoViewSet(viewsets.ModelViewSet):
    """ViewSet for Todo model"""
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['completed', 'due_date']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'title']
    
    def get_queryset(self):
        """Return todos for the current user only"""
        return Todo.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def toggle(self, request, pk=None):
        """Toggle todo completion status"""
        todo = self.get_object()
        serializer = TodoToggleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        todo.completed = serializer.validated_data['completed']
        todo.save()
        
        return Response(TodoSerializer(todo).data)