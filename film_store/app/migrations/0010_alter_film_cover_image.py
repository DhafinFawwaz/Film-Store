# Generated by Django 5.0.7 on 2024-08-13 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_film_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='cover_image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
