# Generated by Django 4.2.4 on 2023-09-05 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_hex_color_tag_color_rename_title_tag_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='unit_of_measure',
            new_name='measurement_unit',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='title',
            new_name='name',
        ),
    ]
