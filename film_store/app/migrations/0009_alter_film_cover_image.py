# Generated by Django 5.0.7 on 2024-08-13 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_review_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
