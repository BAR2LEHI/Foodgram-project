# Generated by Django 4.2.4 on 2023-09-19 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_recipe_recipes_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='recipes_count',
        ),
    ]
