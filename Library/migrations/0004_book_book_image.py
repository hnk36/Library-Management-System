# Generated by Django 5.1.1 on 2024-09-29 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library', '0003_alter_bookcopy_options_alter_genre_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_image',
            field=models.ImageField(blank=True, default='image/placeholder.jfif', null=True, upload_to='image'),
        ),
    ]
