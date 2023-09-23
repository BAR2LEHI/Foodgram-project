from django.db import models
from User.models import FoodGramUser


class Recipe(models.Model):
    author = models.ForeignKey(
        FoodGramUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        null=True
    )
    name = models.CharField(
        max_length=128,
        verbose_name='Название блюда',
        blank=True
    )
    image = models.ImageField(
        verbose_name='Картинка блюда',
        blank=True
    )
    description = models.CharField(
        max_length=128,
        verbose_name='Описание рецепта',
        blank=True
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientToRecipe',
        verbose_name='Ингредиенты рецепта'
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги рецепта'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления в минутах',
        blank=True
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Tag(models.Model):
    name = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='Название тега'
    )
    color = models.CharField(
        max_length=7,
        default='#ffffff',
        unique=True,
        verbose_name='Код цвета'
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        verbose_name='Слаг тега '
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Название ингредиента'
    )
    measurement_unit= models.CharField(
        max_length=64,
        verbose_name='Единица меры'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class IngredientToRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.DO_NOTHING,
        verbose_name='Связь с рецептом'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.DO_NOTHING,
        verbose_name='Связь с ингредиентом'
    )
    quantity = models.IntegerField(
        verbose_name='Количество ингр. в рецепте'
    )

    def __str__(self):
        return f'{self.ingredient} для {self.recipe}'

    class Meta:
        verbose_name = 'Связь рецепта и ингредиента'
        verbose_name_plural = 'Связи рецепта и ингредиента'


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
    is_subscribed = models.BooleanField()


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

    def __str__(self) -> str:
        return 'Список покупок'
