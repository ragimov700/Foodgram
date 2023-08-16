from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='название')
    color = models.CharField(max_length=7, unique=True, verbose_name='цвет')
    slug = models.CharField(max_length=200, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField('Tag', verbose_name='тэги')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='автор')
    name = models.CharField(max_length=200, verbose_name='название')
    text = models.TextField(verbose_name='текст')
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='время приготовления в минутах')
    ingredients = models.ManyToManyField('Ingredient',
                                         through='RecipeIngredient')
    image = models.ImageField(upload_to='recipes/images/',
                              verbose_name='картинка', null=True)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='дата создания')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'рецепт'
        verbose_name_plural = ('рецепты')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='единица измерения')

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE,
                               verbose_name='рецепт')
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE,
                                   verbose_name='ингредиент')
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message='Укажите значение больше 0')],
        verbose_name='количество')

    class Meta:
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'ингредиенты в рецепте'

    def __str__(self):
        return self.ingredient.name


class FavoritesList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='пользователь')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE,
                               verbose_name='рецепт', related_name='favorites')

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='пользователь')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE,
                               verbose_name='рецепт',
                               related_name='shopping_cart')

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'список покупок'

    def __str__(self):
        return f'{self.recipe} в корзине у {self.user}'
