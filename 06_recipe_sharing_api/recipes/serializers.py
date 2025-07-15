from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, RecipeIngredient, Review, Favorite, Collection


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'category', 'unit', 'created_at']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'ingredient_id', 'quantity', 'unit', 'notes']


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class RecipeSerializer(serializers.ModelSerializer):
    chef = ChefSerializer(read_only=True)
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    ingredients_data = RecipeIngredientSerializer(many=True, write_only=True, required=False)
    average_rating = serializers.ReadOnlyField()
    total_time = serializers.ReadOnlyField()
    reviews_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'chef', 'prep_time', 'cook_time',
            'servings', 'difficulty', 'cuisine_type', 'instructions', 'image',
            'is_vegetarian', 'is_vegan', 'is_gluten_free', 'calories_per_serving',
            'recipe_ingredients', 'ingredients_data', 'average_rating', 'total_time',
            'reviews_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['chef', 'created_at', 'updated_at']
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()
    
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients_data', [])
        validated_data['chef'] = self.context['request'].user
        recipe = Recipe.objects.create(**validated_data)
        
        # Add ingredients
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient_data)
        
        return recipe
    
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients_data', None)
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update ingredients if provided
        if ingredients_data is not None:
            instance.recipe_ingredients.all().delete()
            for ingredient_data in ingredients_data:
                RecipeIngredient.objects.create(recipe=instance, **ingredient_data)
        
        return instance


class RecipeSummarySerializer(serializers.ModelSerializer):
    chef_name = serializers.CharField(source='chef.username', read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_time = serializers.ReadOnlyField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'chef_name', 'prep_time', 'cook_time', 'total_time',
            'difficulty', 'cuisine_type', 'servings', 'average_rating', 'image',
            'is_vegetarian', 'is_vegan', 'is_gluten_free', 'created_at'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = ChefSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'recipe', 'reviewer', 'rating', 'comment', 'created_at']
        read_only_fields = ['reviewer', 'created_at']
    
    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = RecipeSummarySerializer(read_only=True)
    recipe_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'recipe', 'recipe_id', 'created_at']
        read_only_fields = ['user', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CollectionSerializer(serializers.ModelSerializer):
    recipes = RecipeSummarySerializer(many=True, read_only=True)
    recipe_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True, 
        required=False
    )
    recipes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Collection
        fields = [
            'id', 'name', 'description', 'user', 'recipes', 'recipe_ids',
            'is_public', 'recipes_count', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']
    
    def get_recipes_count(self, obj):
        return obj.recipes.count()
    
    def create(self, validated_data):
        recipe_ids = validated_data.pop('recipe_ids', [])
        validated_data['user'] = self.context['request'].user
        collection = Collection.objects.create(**validated_data)
        
        if recipe_ids:
            collection.recipes.set(recipe_ids)
        
        return collection
    
    def update(self, instance, validated_data):
        recipe_ids = validated_data.pop('recipe_ids', None)
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update recipes if provided
        if recipe_ids is not None:
            instance.recipes.set(recipe_ids)
        
        return instance
