from rest_framework import serializers
from api.models import Recipe, Tag, Ingredient, Subscription, FavoriteRecipe, IngredientToRecipe, ShoppingList
from User.models import FoodGramUser



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
    

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredToRecipeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = IngredientToRecipe
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredToRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSerializer(serializers.ModelSerializer):
    recipes = RecipeShortSerializer(many=True)

    class Meta:
        model = FoodGramUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'recipes', 'recipes_count')


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError('Новый пароль не должен совпадать со старым')
        return data


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('following', 'followers')

    def validate(self, data):
        user = data['followers'].pk
        author = data['following'].pk
        if user == author:
            raise serializers.ValidationError('Нельзя подписаться на самого себя')
        if Subscription.objects.filter(
            following__id=author,
            followers__id=user
        ).exists():
            raise serializers.ValidationError('Вы уже подписаны на этого автора')
        return data
    
    def create(self, validated_data):
        subscribe = Subscription.objects.create(**validated_data, is_subscribed=True)
        return subscribe


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'favorite_recipe')
    
    def validate(self, data):
        user = data['user'].pk
        recipe = data['favorite_recipe'].pk
        if FavoriteRecipe.objects.filter(
            user__id=user,
            favorite_recipe__id=recipe
        ).exists():
            raise serializers.ValidationError('Этот рецепт уже у вас в избранном')
        return data


class ShoppingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingList
        fields = ('user', 'shop_recipe')

    def validate(self, data):
        user = data['user'].pk
        recipe = data['shop_recipe'].pk
        if ShoppingList.objects.filter(
            user__id=user,
            shop_recipe=recipe
        ).exists():
            raise serializers.ValidationError('Этот рецепт уже есть в списке покупок')
        return data


class TestIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name',)
        model = Ingredient