from django.urls import include, path
from rest_framework import routers

from .views import RecipesViewSet, TagsViewSet, IngredientViewSet, UsersViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('recipes', RecipesViewSet, basename='recipes')
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('', include(router_v1.urls)),
]


