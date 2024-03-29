import csv

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import (FavoriteRecipe, Ingredient, IngredientToRecipe, Recipe,
                        ShoppingList, Subscription, Tag)
from users.models import FoodGramUser

from .filters import IngredientStartsWithFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import AuthorOrReadOnlyPermission
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PasswordSerializer, RecipeGetSerializer,
                          RecipePostSerializer, ShoppingListSerializer,
                          SubscribeSerializer, TagSerializer,
                          UserPostSerializer, UserSerializer,
                          UserShortSerializer)


class RecipesViewSet(viewsets.ModelViewSet):
    """Viewset для обработки всех запросов к Recipe"""
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = RecipeGetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (AuthorOrReadOnlyPermission, )
    pagination_class = CustomPagination

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        """Статический метод POST для actions"""
        if serializers == FavoriteSerializer:
            data = {
                'user': request.user.pk,
                'favorite_recipe': pk
            }
        else:
            data = {
                'user': request.user.pk,
                'shop_recipe': pk
            }
        serializer = serializers(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_method_for_actions(model, user, recipe):
        """Статический метод DELETE для actions"""
        if model == FavoriteRecipe:
            model.objects.filter(
                user=user,
                favorite_recipe=recipe
            ).delete()
        else:
            model.objects.filter(
                user=user,
                shop_recipe=recipe
            ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def favorite(self, request, pk):
        """Метод добавления рецепта в избранное"""
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'DELETE':
            return self.delete_method_for_actions(FavoriteRecipe, user, recipe)
        return self.post_method_for_actions(request, pk, FavoriteSerializer)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def shopping_cart(self, request, pk):
        """Метод добавления рецепта в список покупок"""
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'DELETE':
            return self.delete_method_for_actions(ShoppingList, user, recipe)
        return self.post_method_for_actions(
            request, pk, ShoppingListSerializer
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        """Метод для скачивания файла с количеством необходимых ингредиентов"""
        ingredients = IngredientToRecipe.objects.filter(
            recipe__shop_recipe__user=self.request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename="shoplist.csv"'
            }
        )
        writer = csv.writer(response, delimiter='-')
        writer.writerow(['Наименование', 'Единица измерения', 'Количество'])
        for ingredient in ingredients:
            writer.writerow(
                [ingredient['ingredient__name'],
                 ingredient['ingredient__measurement_unit'],
                 ingredient['amount']]
            )
        return response

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        return RecipePostSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        print(instance.author)
        if instance.author != self.request.user:
            raise serializers.ValidationError(
                'Вы не можете удалить чужой рецепт'
            )
        instance.delete()


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для обработки GET-запросов к Tags"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для обработки GET-запросов к Ingredients"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientStartsWithFilter


class UsersViewSet(viewsets.ModelViewSet):
    """Viewset для обработки GET, POST - запросов к FoodGramUser"""
    queryset = FoodGramUser.objects.all()
    serializer_class = UserShortSerializer
    pagination_class = CustomPagination
    permission_classes = (AllowAny, )

    @action(detail=False, methods=['post'])
    def set_password(self, request):
        """Метод для изменения пароля пользователя"""
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(
                serializer.validated_data['current_password']
            ):
                return Response({'current_password': 'Неверный пароль'})
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, permission_classes=[IsAuthenticated, ])
    def subscriptions(self, request):
        """Метод для отображения подписок пользователя"""
        queryset = FoodGramUser.objects.filter(
            following__followers=request.user
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(
                page,
                context={'request': self.request},
                many=True
            )
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(
            queryset,
            context={'request': self.request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post_method_for_subscribe(request, pk, serializers):
        """Статический метод POST для подписки на пользователя"""
        data = {
            'following': pk,
            'followers': request.user.pk
        }
        serializer = serializers(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete_method_for_subscribe(model, user, author):
        """Статический метод DELETE для подписки на пользователя"""
        model.objects.filter(
            following=author,
            followers=user
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def subscribe(self, request, pk):
        """Метод для подписки и отписки на пользователей"""
        user = self.request.user
        author = get_object_or_404(FoodGramUser, id=pk)
        if request.method == 'DELETE':
            return self.delete_method_for_subscribe(Subscription, user, author)
        return self.post_method_for_subscribe(request, pk, SubscribeSerializer)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        return UserPostSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'me':
            return self.request.user
        return super(UsersViewSet, self).get_object()
