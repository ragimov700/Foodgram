# Generated by Django 3.2 on 2023-08-09 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20230802_1414'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppinglist',
            options={'verbose_name': 'список покупок', 'verbose_name_plural': 'список покупок'},
        ),
    ]