# Generated by Django 5.1.1 on 2024-09-24 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelTable(
            name='book',
            table='books',
        ),
    ]
