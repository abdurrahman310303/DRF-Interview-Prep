# Recipe Sharing API - DRF Interview Prep Project

## 🎯 Project Overview

A comprehensive Django REST Framework API for a recipe sharing platform that demonstrates:
- **Content Management System** patterns
- **Rating and Review Systems**
- **Social Features** (likes, follows, favorites)
- **Advanced Search** with ingredient-based filtering
- **Image Upload and Processing**
- **Nutritional Data Management**

## 🚀 Features

### **Recipe Management**
- Create, edit, delete recipes
- Step-by-step cooking instructions
- Ingredient management with quantities
- Cooking time and difficulty levels
- Recipe categories (Appetizer, Main Course, Dessert, etc.)
- Multiple recipe images

### **User Profiles**
- Chef profiles with bio and specialties
- Recipe collections and favorites
- Follow/unfollow other chefs
- Personal recipe books
- Cooking skill levels

### **Social Features**
- Rate and review recipes (1-5 stars)
- Like/unlike recipes
- Comment on recipes
- Share recipes
- Recipe recommendations

### **Advanced Search**
- Search by ingredients (have/don't have)
- Filter by dietary restrictions (vegan, gluten-free, etc.)
- Filter by cooking time, difficulty, rating
- Cuisine type filtering
- Nutritional information search

### **Meal Planning**
- Create weekly meal plans
- Shopping list generation from recipes
- Nutritional tracking
- Portion calculator

## 🏗️ System Architecture

### **Database Models**
- **User**: Extended user with chef profile
- **Recipe**: Main recipe model with metadata
- **Ingredient**: Ingredient database with nutritional info
- **RecipeIngredient**: Junction table with quantities
- **Instruction**: Step-by-step cooking instructions
- **Review**: Recipe reviews and ratings
- **Collection**: User recipe collections
- **MealPlan**: Weekly meal planning

## 📁 Project Structure

```
06_recipe_sharing_api/
├── recipe_api/               # Main Django project
│   ├── settings.py           # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── recipes/                  # Recipe management app
│   ├── models.py            # Recipe, Instruction models
│   ├── serializers.py       # Recipe serializers
│   ├── views.py             # Recipe ViewSets
│   ├── filters.py           # Custom filters
│   └── admin.py             # Admin interface
├── ingredients/              # Ingredient management app
│   ├── models.py            # Ingredient model
│   ├── serializers.py       # Ingredient serializers
│   ├── views.py             # Ingredient ViewSet
│   └── admin.py             # Admin interface
├── profiles/                 # User profile app
│   ├── models.py            # Chef profile model
│   ├── serializers.py       # Profile serializers
│   ├── views.py             # Profile ViewSet
│   └── admin.py             # Admin interface
├── social/                   # Social features app
│   ├── models.py            # Review, Like, Follow models
│   ├── serializers.py       # Social serializers
│   ├── views.py             # Social ViewSets
│   └── admin.py             # Admin interface
├── meal_plans/               # Meal planning app
│   ├── models.py            # MealPlan model
│   ├── serializers.py       # MealPlan serializers
│   ├── views.py             # MealPlan ViewSet
│   └── utils.py             # Meal planning utilities
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🛠️ Installation & Setup

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **3. Load Sample Data**
```bash
python manage.py loaddata fixtures/ingredients.json
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/sample_recipes.json
```

### **4. Create Superuser**
```bash
python manage.py createsuperuser
```

### **5. Run Development Server**
```bash
python manage.py runserver
```

## 🌐 API Endpoints

### **Recipes**
- `GET /api/recipes/` - List recipes with filtering
- `POST /api/recipes/` - Create new recipe
- `GET /api/recipes/{id}/` - Get recipe details
- `PUT /api/recipes/{id}/` - Update recipe
- `DELETE /api/recipes/{id}/` - Delete recipe
- `POST /api/recipes/{id}/like/` - Like/unlike recipe
- `GET /api/recipes/trending/` - Trending recipes
- `GET /api/recipes/recommended/` - Personalized recommendations

### **Ingredients**
- `GET /api/ingredients/` - List ingredients
- `POST /api/ingredients/` - Add new ingredient
- `GET /api/ingredients/{id}/` - Get ingredient details
- `GET /api/ingredients/search/?q=tomato` - Search ingredients
- `GET /api/ingredients/{id}/nutrition/` - Nutritional information

### **Reviews & Ratings**
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Add review
- `GET /api/reviews/{id}/` - Get review details
- `PUT /api/reviews/{id}/` - Update review
- `DELETE /api/reviews/{id}/` - Delete review

### **User Profiles**
- `GET /api/profiles/` - List chef profiles
- `GET /api/profiles/{id}/` - Get profile details
- `PUT /api/profiles/{id}/` - Update profile
- `GET /api/profiles/{id}/recipes/` - User's recipes
- `POST /api/profiles/{id}/follow/` - Follow/unfollow chef

### **Collections**
- `GET /api/collections/` - List recipe collections
- `POST /api/collections/` - Create collection
- `GET /api/collections/{id}/` - Get collection details
- `POST /api/collections/{id}/add-recipe/` - Add recipe to collection
- `DELETE /api/collections/{id}/remove-recipe/` - Remove recipe

### **Meal Plans**
- `GET /api/meal-plans/` - List meal plans
- `POST /api/meal-plans/` - Create meal plan
- `GET /api/meal-plans/{id}/` - Get meal plan details
- `GET /api/meal-plans/{id}/shopping-list/` - Generate shopping list
- `GET /api/meal-plans/{id}/nutrition/` - Nutritional summary

### **Search & Discovery**
- `GET /api/search/?q=pasta` - Recipe search
- `GET /api/search/by-ingredients/?have=tomato,onion&exclude=meat` - Ingredient-based search
- `GET /api/recipes/by-cuisine/?cuisine=italian` - Cuisine-based filtering
- `GET /api/recipes/by-diet/?diet=vegan` - Dietary restriction filtering

## 📊 Data Models

### **Recipe Model**
```python
class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient')
    prep_time = models.PositiveIntegerField()  # minutes
    cook_time = models.PositiveIntegerField()  # minutes
    servings = models.PositiveIntegerField(default=1)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    cuisine = models.CharField(max_length=50)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    calories_per_serving = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **Ingredient Model**
```python
class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    calories_per_100g = models.FloatField(null=True, blank=True)
    protein_per_100g = models.FloatField(null=True, blank=True)
    carbs_per_100g = models.FloatField(null=True, blank=True)
    fat_per_100g = models.FloatField(null=True, blank=True)
    fiber_per_100g = models.FloatField(null=True, blank=True)
    is_allergen = models.BooleanField(default=False)
    allergen_type = models.CharField(max_length=50, blank=True)
```

### **Review Model**
```python
class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['recipe', 'reviewer']
```

## 🧪 Testing the API

### **1. Create Recipe**
```bash
curl -X POST http://localhost:8000/api/recipes/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Spaghetti Carbonara",
    "description": "Classic Italian pasta dish",
    "prep_time": 10,
    "cook_time": 15,
    "servings": 4,
    "difficulty": "medium",
    "cuisine": "italian",
    "category": 1,
    "is_vegetarian": false,
    "ingredients": [
      {"ingredient_id": 1, "quantity": "400g"},
      {"ingredient_id": 2, "quantity": "200g"},
      {"ingredient_id": 3, "quantity": "4 pieces"}
    ],
    "instructions": [
      {"step_number": 1, "instruction": "Boil pasta water"},
      {"step_number": 2, "instruction": "Cook pasta al dente"},
      {"step_number": 3, "instruction": "Mix eggs and cheese"}
    ]
  }'
```

### **2. Search by Ingredients**
```bash
curl -X GET "http://localhost:8000/api/search/by-ingredients/?have=pasta,eggs&exclude=meat"
```

### **3. Add Review**
```bash
curl -X POST http://localhost:8000/api/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "recipe": 1,
    "rating": 5,
    "comment": "Absolutely delicious! Easy to follow instructions."
  }'
```

## 🔍 Advanced Features

### **Smart Recommendations**
- Based on user's favorite cuisines
- Considering dietary restrictions
- Seasonal ingredient availability
- Cooking skill level matching

### **Nutritional Analysis**
- Automatic calorie calculation
- Macro/micronutrient breakdown
- Allergen warnings
- Dietary compliance checking

### **Social Engagement**
- Recipe trending algorithm
- Chef popularity ranking
- Community challenges
- Recipe contests

## 📈 Filtering & Search Options

### **Recipe Filtering**
- `?cuisine=italian,mexican` - Filter by cuisine
- `?difficulty=easy` - Filter by difficulty
- `?max_time=30` - Recipes under 30 minutes
- `?dietary=vegan,gluten_free` - Dietary restrictions
- `?rating__gte=4` - Minimum rating
- `?servings__lte=2` - Maximum servings

### **Advanced Search**
- `?ingredients__contains=tomato` - Must contain ingredient
- `?ingredients__excludes=nuts` - Must not contain
- `?calories__lt=500` - Low calorie recipes
- `?prep_time__lt=15` - Quick prep recipes

## 🚀 Next Steps & Enhancements

### **Immediate Improvements**
1. **Recipe Video Support** with thumbnail generation
2. **Advanced Meal Planning** with nutritional goals
3. **Recipe Import** from popular cooking websites
4. **Mobile App Integration** with barcode scanning

### **Advanced Features**
1. **AI-Powered Recipe Generation** from available ingredients
2. **Computer Vision** for recipe image analysis
3. **Voice Commands** for hands-free cooking
4. **Integration with Smart Kitchen Appliances**
5. **Augmented Reality** cooking assistance

## 🎓 Learning Outcomes

This project demonstrates:
- **Content Management Systems** with complex relationships
- **Social Platform Features** implementation
- **Advanced Search and Filtering** techniques
- **Rating and Review Systems** design
- **Nutritional Data Management**
- **Image Upload and Processing** workflows
- **Recommendation Engine** basics
- **Community-driven Content** moderation

## 💡 Interview Topics Covered

- **Complex Many-to-Many relationships** with through models
- **Advanced Django ORM** queries and aggregations
- **Custom API actions** and business logic
- **Image handling and media management**
- **Search optimization** techniques
- **Social features** implementation
- **Data analysis and recommendations**
- **Performance optimization** for content platforms

---

**Perfect for demonstrating social platform and content management skills!** 🍳
