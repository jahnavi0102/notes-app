# Generated by Django 5.0.1 on 2024-01-04 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
