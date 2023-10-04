import django_filters

from api.models import Ingredient, Recipe


class RecipeFilter(django_filters.FilterSet):
    """Фильтр для рецептов"""
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    is_favorited = django_filters.BooleanFilter(
        method='filter_is_favorited'
    )
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        lookup_expr='icontains'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'is_in_shopping_cart', 'tags')

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(
                shop_recipe__user=self.request.user.id
            )
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(
                favorite_recipes__user=self.request.user
            )
        return queryset


class IngredientStartsWithFilter(django_filters.FilterSet):
    """Фильтр для ингредиентов"""
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
