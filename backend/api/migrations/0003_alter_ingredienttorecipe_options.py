# Generated by Django 4.2.4 on 2023-09-02 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_ingredient_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredienttorecipe',
            options={'verbose_name': 'Связь рецепта и ингредиента', 'verbose_name_plural': 'Связи рецепта и ингредиента'},
        ),
    ]