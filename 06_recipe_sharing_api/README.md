# Recipe Sharing Platform API

A social recipe sharing Django REST Framework API with advanced search and meal planning features.

## Features

- **Recipe Management**: Create recipes with ingredients and step-by-step instructions
- **Social Features**: Follow chefs, rate recipes, create collections
- **Advanced Search**: Search by ingredients, dietary restrictions, cuisine type
- **Meal Planning**: Weekly meal plans and shopping list generation
- **Nutritional Info**: Track calories and nutritional data

## Tech Stack

- Django REST Framework
- PostgreSQL/SQLite
- Django Taggit for tagging
- JWT Authentication
- Image handling for recipe photos

## Installation

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API Endpoints

- `/api/recipes/` - Recipe management
- `/api/ingredients/` - Ingredient database  
- `/api/profiles/` - Chef profiles
- `/api/reviews/` - Recipe reviews and ratings
- `/api/meal-plans/` - Meal planning

## Learning Focus

- Content management system patterns
- Social platform features (follow, like, rate)
- Advanced search with multiple criteria
- Many-to-many relationships with through models
