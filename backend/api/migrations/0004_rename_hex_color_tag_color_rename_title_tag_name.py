# Generated by Django 4.2.4 on 2023-09-05 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_ingredienttorecipe_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='hex_color',
            new_name='color',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='title',
            new_name='name',
        ),
    ]
