from colorfield.fields import ColorField
from django.db import models

from users.models import FoodGramUser


class Recipe(models.Model):
    author = models.ForeignKey(
        FoodGramUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название блюда'
    )
    image = models.ImageField(
        verbose_name='Картинка блюда',
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientToRecipe',
        verbose_name='Ингредиенты рецепта',
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги рецепта',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления в минутах',
    )

    class Meta:
        ordering = ['id', ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        verbose_name='Название тега'
    )
    color = ColorField(
        default='#FF0000',
        unique=True,
        verbose_name='Код цвета'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг тега'
    )

    class Meta:
        ordering = ['id', ]
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        verbose_name='Единица меры'
    )

    class Meta:
        ordering = ['id', ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class IngredientToRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Связь с рецептом'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Связь с ингредиентом'
    )
    amount = models.IntegerField(
        verbose_name='Количество ингр. в рецепте'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_to_ingredient_unique'
            )
        ]
        ordering = ['id', ]
        verbose_name = 'Связь рецепта и ингредиента'
        verbose_name_plural = 'Связи рецепта и ингредиента'

    def __str__(self):
        return f'{self.ingredient} для {self.recipe}'


class Subscription(models.Model):
    following = models.ForeignKey(
        FoodGramUser,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Подписан на *'
    )
    followers = models.ForeignKey(
        FoodGramUser,
        related_name='followers',
        on_delete=models.CASCADE,
        verbose_name='Подписчики',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'followers'],
                name='unique_subscription'
            )
        ]
        ordering = ['id', ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.followers} подписан на {self.following}'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        FoodGramUser,
        related_name='user_favorite',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        related_name='favorite_recipes',
        on_delete=models.CASCADE,
        verbose_name='Избранный рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'favorite_recipe'],
                name='unique_favorite'
            )
        ]
        ordering = ['id', ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return 'Избранные рецепты'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        FoodGramUser,
        related_name='user_shop',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    shop_recipe = models.ForeignKey(
        Recipe,
        related_name='shop_recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт в списке покупок'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'shop_recipe'],
                name='unique_shop_recipe'
            )
        ]
        ordering = ['id', ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self) -> str:
        return 'Список покупок'
