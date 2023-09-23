from django.contrib import admin

from .models import Recipe, Tag, Ingredient, IngredientToRecipe, Subscription, FavoriteRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'description',
        'cooking_time',
    )
    list_filter = (
        'author',
        'name',
        'tags'
    )
    search_fields = (
        'author',
        'tags'
    )
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
        'color'
    )
    list_filter = (
        'name',
    )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = (
        'name',
    )
    empty_value_display = '-пусто-'


@admin.register(IngredientToRecipe)
class IngToRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'quantity',
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'followers',
        'following',
        'is_subscribed'
    )


@admin.register(FavoriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'favorite_recipe'
    )
