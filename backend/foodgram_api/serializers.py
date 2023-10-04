import webcolors
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.models import (FavoriteRecipe, Ingredient, IngredientToRecipe, Recipe,
                        ShoppingList, Subscription, Tag)
from users.models import FoodGramUser


class Hex2NameColor(serializers.Field):
    """Поле для преобразования hex кода цвета в название"""
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class UserShortSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для модели User"""
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = FoodGramUser
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return request.user.is_authenticated and Subscription.objects.filter(
            followers=request.user,
            following__id=obj.id
        ).exists()


class RecipeShortSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для модели Recipe"""
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name',
            'image', 'cooking_time'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор GET-запросов к модели User"""
    recipes = RecipeShortSerializer(many=True)
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta:
        model = FoodGramUser
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'is_subscribed',
            'recipes', 'recipes_count'
        )

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author__id=obj.id).count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return request.user.is_authenticated and Subscription.objects.filter(
            followers=request.user,
            following__id=obj.id
        ).exists()


class UserPostSerializer(serializers.ModelSerializer):
    """Сериализатор POST-запросов к модели User"""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z', allow_blank=False
    )

    class Meta:
        model = FoodGramUser
        fields = (
            'email', 'id',
            'username', 'first_name',
            'last_name', 'password'
        )
        read_only_fields = ('id',)

    @transaction.atomic
    def create(self, validated_data):
        user = FoodGramUser.objects.create(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        ret = super(UserPostSerializer, self).to_representation(instance)
        ret.pop('password')
        return ret


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag"""
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = (
            'id', 'name',
            'color', 'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient"""
    class Meta:
        model = Ingredient
        fields = (
            'id', 'name',
            'measurement_unit',
        )


class IngredToRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для промежуточной модели IngredientToRecipe"""
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientToRecipe
        fields = (
            'id', 'name',
            'measurement_unit', 'amount'
        )


class AddIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления игредиентов в рецепт"""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientToRecipe
        fields = (
            'id', 'amount'
        )


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для GET-запросов к Recipe"""
    tags = TagSerializer(
        many=True, read_only=True
    )
    author = UserShortSerializer(
        many=False, read_only=True
    )
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags',
            'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image',
            'text', 'cooking_time'
        )
        read_only_fields = ('author', )

    def get_ingredients(self, obj):
        ingredients = IngredientToRecipe.objects.filter(recipe=obj)
        return IngredToRecipeSerializer(ingredients, many=True).data

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return request.user.is_authenticated and ShoppingList.objects.filter(
            user=request.user, shop_recipe__id=obj.id
        ).exists()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return request.user.is_authenticated and FavoriteRecipe.objects.filter(
            user=request.user,
            favorite_recipe__id=obj.id
        ).exists()


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для POST, PATCH - запросов к модели Recipe"""
    ingredients = AddIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        read_only=False
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags',
            'image', 'name',
            'text', 'cooking_time'
        )
        read_only_fields = ('author',)

    def validate(self, data):
        name = data['name']
        ingredients = data['ingredients']
        tags = data['tags']
        if not tags:
            raise serializers.ValidationError(
                'Обязательно нужно указать хотя бы 1 тег'
            )
        for tag in tags:
            if not Tag.objects.filter(id=tag.id).exists():
                raise serializers.ValidationError(
                    'Указанного вами тега не существует'
                )
        if not ingredients:
            raise serializers.ValidationError(
                'Обязательно должен быть хотя бы 1 ингредиент'
            )
        for ingredient in ingredients:
            if not Ingredient.objects.filter(id=ingredient['id']).exists():
                raise serializers.ValidationError(
                    'Указанного вами игредиента не существует'
                )
        if Recipe.objects.filter(name=name).exists():
            raise serializers.ValidationError('Такой рецепт есть уже')
        return data

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Невозможно приготовить блюдо меньше чем за минуту!'
            )
        return value

    @staticmethod
    def create_ingredients(recipe, ingredients):
        IngredientToRecipe.objects.bulk_create(
            [
                IngredientToRecipe(
                    ingredient=Ingredient.objects.get(
                        id=ingredient['id']
                    ),
                    recipe=recipe,
                    amount=ingredient['amount']
                ) for ingredient in ingredients
            ]
        )

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            **validated_data
        )
        self.create_ingredients(
            recipe=recipe,
            ingredients=ingredients
        )
        recipe.tags.set(tags)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(
            recipe=instance,
            ingredients=ingredients
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeGetSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class PasswordSerializer(serializers.Serializer):
    """Сериализатор для изменения пароля"""
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] == data['current_password']:
            raise serializers.ValidationError(
                'Новый пароль не должен совпадать со старым'
            )
        return data


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок"""
    class Meta:
        model = Subscription
        fields = (
            'following', 'followers'
        )

    def validate(self, data):
        user = data['followers']
        author = data['following']
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        if Subscription.objects.filter(
            following=author,
            followers=user
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора'
            )
        return data

    def to_representation(self, instance):
        return UserSerializer(
            instance.following,
            context={'request': self.context.get('request')}
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецепта в избранное"""

    class Meta:
        model = FavoriteRecipe
        fields = (
            'user', 'favorite_recipe'
        )

    def validate(self, data):
        user = data['user'].pk
        recipe = data['favorite_recipe'].pk
        if FavoriteRecipe.objects.filter(
            user__id=user,
            favorite_recipe__id=recipe
        ).exists():
            raise serializers.ValidationError(
                'Этот рецепт уже у вас в избранном'
            )
        return data

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.favorite_recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingListSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецепта в список покупок"""

    class Meta:
        model = ShoppingList
        fields = (
            'user', 'shop_recipe'
        )

    def validate(self, data):
        user = data['user'].pk
        recipe = data['shop_recipe'].pk
        if ShoppingList.objects.filter(
            user__id=user,
            shop_recipe=recipe
        ).exists():
            raise serializers.ValidationError(
                'Этот рецепт уже есть в списке покупок'
            )
        return data

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.shop_recipe,
            context={'request': self.context.get('request')}
        ).data
