# Generated by Django 5.0.7 on 2024-08-11 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_generaluser_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
