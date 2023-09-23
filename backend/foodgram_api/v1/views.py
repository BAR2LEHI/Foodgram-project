from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from reportlab.pdfgen import canvas 
from django.http import HttpResponse
from .renderers import TxtREnder
from io import BytesIO
import csv
from django.db.models import Sum
from .utils import CustomPagination
from api.models import Ingredient, IngredientToRecipe, Recipe, Tag, Subscription, FavoriteRecipe, ShoppingList
from User.models import FoodGramUser

from .serializers import (IngredientSerializer, PasswordSerializer,
                          RecipeSerializer, TagSerializer, UserSerializer, SubscribeSerializer, FavoriteSerializer, RecipeShortSerializer, ShoppingListSerializer, TestIngredientSerializer)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = LimitOffsetPagination

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            'user': user.pk,
            'favorite_recipe': recipe.pk
        }
        serializer = FavoriteSerializer(data=data)
        if request.method == 'DELETE':
            if not FavoriteRecipe.objects.filter(
                user=user,
                favorite_recipe=recipe
            ).exists():
                raise serializers.ValidationError('Этого рецепта и так нет в избранном')
            FavoriteRecipe.objects.filter(
                user=user,
                favorite_recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if serializer.is_valid():
            serializer.save()
            serializer = RecipeShortSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            'user': user.pk,
            'shop_recipe': recipe.pk
        }
        serializer = ShoppingListSerializer(data=data)
        if request.method == 'DELETE':
            if not ShoppingList.objects.filter(
                user=user,
                shop_recipe=recipe
            ).exists():
                raise serializers.ValidationError('Рецепта и так не было в списке покупок')
            ShoppingList.objects.filter(
                user=user,
                shop_recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if serializer.is_valid():
            serializer.save()
            serializer = RecipeShortSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        ingredients = IngredientToRecipe.objects.filter(
            recipe__shop_recipe__user=self.request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('quantity'))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        writer = csv.writer(response, delimiter='-')
        writer.writerow(['Наименование', 'Единица измерения', 'Количество'])
        for ingredient in ingredients:
            print(ingredient)
            writer.writerow(
                [ingredient['ingredient__name'],
                 ingredient['ingredient__measurement_unit'],
                 ingredient['amount']]
            )
        return response
    

    def perform_create(self, serializer):
        user = self.request.user
        user.recipes_count = Recipe.objects.filter(author=self.request.user).count()
        user.save()
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = LimitOffsetPagination


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = FoodGramUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': 'Wrong password'})
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False)
    def subscriptions(self, request):
        queryset = FoodGramUser.objects.filter(following__followers=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, pk):
        user = self.request.user
        author = get_object_or_404(FoodGramUser, id=pk)
        data = {
            'following': author.pk,
            'followers': user.pk
        }
        serializer = SubscribeSerializer(data=data)
        if request.method == 'DELETE':
            if not Subscription.objects.filter(
                followers=user,
                following=author
            ).exists():
                raise serializers.ValidationError(
                    'Вы и так не подписаны на этого автора'
                )
            Subscription.objects.get(
                followers=user,
                following=author
            ).delete()
            return Response({'status': 'вы успешно отписались'}, status=status.HTTP_204_NO_CONTENT)
        if serializer.is_valid():
            serializer.save()
            serializer = UserSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'me':
            return self.request.user
        return super(UsersViewSet, self).get_object()
