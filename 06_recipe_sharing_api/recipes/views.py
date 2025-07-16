from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg
from .models import Recipe, Ingredient, Review, Favorite, Collection
from .serializers import (
    RecipeSerializer, RecipeSummarySerializer, IngredientSerializer,
    ReviewSerializer, FavoriteSerializer, CollectionSerializer
)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('chef').prefetch_related('recipe_ingredients__ingredient', 'reviews').all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'chef__username', 'cuisine_type']
    filterset_fields = ['difficulty', 'cuisine_type', 'is_vegetarian', 'is_vegan', 'is_gluten_free']
    ordering_fields = ['created_at', 'prep_time', 'cook_time', 'servings']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeSummarySerializer
        return RecipeSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        
        # Filter by chef
        chef = self.request.query_params.get('chef')
        if chef:
            queryset = queryset.filter(chef__username__icontains=chef)
        
        # Filter by ingredient
        ingredient = self.request.query_params.get('ingredient')
        if ingredient:
            queryset = queryset.filter(
                recipe_ingredients__ingredient__name__icontains=ingredient
            ).distinct()
        
        # Filter by max prep time
        max_prep_time = self.request.query_params.get('max_prep_time')
        if max_prep_time:
            queryset = queryset.filter(prep_time__lte=max_prep_time)
        
        # Filter by max total time
        max_total_time = self.request.query_params.get('max_total_time')
        if max_total_time:
            queryset = queryset.filter(prep_time__plus__cook_time__lte=max_total_time)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular recipes based on reviews"""
        popular_recipes = self.queryset.annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(avg_rating__gte=4.0).order_by('-avg_rating')[:20]
        
        serializer = RecipeSummarySerializer(popular_recipes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def quick(self, request):
        """Get quick recipes (total time <= 30 minutes)"""
        quick_recipes = self.queryset.filter(prep_time__plus__cook_time__lte=30)
        page = self.paginate_queryset(quick_recipes)
        if page is not None:
            serializer = RecipeSummarySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = RecipeSummarySerializer(quick_recipes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """Add recipe to favorites"""
        recipe = self.get_object()
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        
        if created:
            return Response({'message': 'Recipe added to favorites'})
        else:
            return Response(
                {'message': 'Recipe already in favorites'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unfavorite(self, request, pk=None):
        """Remove recipe from favorites"""
        recipe = self.get_object()
        try:
            favorite = Favorite.objects.get(user=request.user, recipe=recipe)
            favorite.delete()
            return Response({'message': 'Recipe removed from favorites'})
        except Favorite.DoesNotExist:
            return Response(
                {'message': 'Recipe not in favorites'},
                status=status.HTTP_400_BAD_REQUEST
            )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category']
    ordering_fields = ['name', 'category', 'created_at']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all ingredient categories"""
        categories = Ingredient.objects.values_list('category', flat=True).distinct()
        return Response(list(categories))


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('reviewer', 'recipe').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rating', 'recipe']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Users can only see all reviews, but can only modify their own
        if self.action in ['update', 'partial_update', 'destroy']:
            return self.queryset.filter(reviewer=self.request.user)
        return self.queryset


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('recipe__chef')


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        if self.action == 'list':
            # Show user's collections and public collections
            return Collection.objects.filter(
                Q(user=self.request.user) | Q(is_public=True)
            ).prefetch_related('recipes')
        return Collection.objects.filter(user=self.request.user).prefetch_related('recipes')
    
    @action(detail=True, methods=['post'])
    def add_recipe(self, request, pk=None):
        """Add recipe to collection"""
        collection = self.get_object()
        recipe_id = request.data.get('recipe_id')
        
        if not recipe_id:
            return Response(
                {'error': 'recipe_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            collection.recipes.add(recipe)
            return Response({'message': 'Recipe added to collection'})
        except Recipe.DoesNotExist:
            return Response(
                {'error': 'Recipe not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['delete'])
    def remove_recipe(self, request, pk=None):
        """Remove recipe from collection"""
        collection = self.get_object()
        recipe_id = request.data.get('recipe_id')
        
        if not recipe_id:
            return Response(
                {'error': 'recipe_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            collection.recipes.remove(recipe)
            return Response({'message': 'Recipe removed from collection'})
        except Recipe.DoesNotExist:
            return Response(
                {'error': 'Recipe not found'},
                status=status.HTTP_404_NOT_FOUND
            )
