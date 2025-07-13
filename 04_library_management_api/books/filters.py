import django_filters
from django.db.models import Q
from .models import Book, Author, Genre


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(method='filter_by_author')
    genre = django_filters.CharFilter(method='filter_by_genre')
    publication_year = django_filters.NumberFilter(field_name='publication_date__year')
    publication_year_gte = django_filters.NumberFilter(field_name='publication_date__year', lookup_expr='gte')
    publication_year_lte = django_filters.NumberFilter(field_name='publication_date__year', lookup_expr='lte')
    available_only = django_filters.BooleanFilter(method='filter_available_only')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    language = django_filters.CharFilter(lookup_expr='iexact')
    
    class Meta:
        model = Book
        fields = {
            'title': ['icontains', 'exact'],
            'isbn': ['exact', 'icontains'],
            'publisher': ['icontains', 'exact'],
            'pages': ['exact', 'gte', 'lte'],
            'publication_date': ['exact', 'year', 'year__gte', 'year__lte'],
        }
    
    def filter_by_author(self, queryset, name, value):
        return queryset.filter(
            Q(authors__name__icontains=value)
        ).distinct()
    
    def filter_by_genre(self, queryset, name, value):
        return queryset.filter(
            Q(genres__name__icontains=value)
        ).distinct()
    
    def filter_available_only(self, queryset, name, value):
        if value:
            return queryset.filter(available_copies__gt=0)
        return queryset
