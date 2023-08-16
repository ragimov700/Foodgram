from django_filters.rest_framework import (AllValuesMultipleFilter,
                                           BooleanFilter, FilterSet)
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = BooleanFilter(field_name='is_favorited',
                                 method='filter_favorited')
    is_in_shopping_cart = BooleanFilter(field_name='is_in_shopping_cart',
                                        method='filter_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author',)

    def filter_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)

    def filter_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
