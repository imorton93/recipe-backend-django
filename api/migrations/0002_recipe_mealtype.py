# Generated by Django 5.1.6 on 2025-02-23 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='mealType',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack'), ('Dessert', 'Dessert'), ('Drinks', 'Drinks')], default='Dinner', max_length=50),
        ),
    ]
