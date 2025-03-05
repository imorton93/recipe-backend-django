from django.db import models
    

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

# Create your models here.
class Recipe(models.Model):
    MEAL_TYPE_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
        ('Dessert', 'Dessert'),
        ('Drinks', 'Drinks'),
    ]


    name = models.CharField(max_length=255)
    ingredients = models.JSONField()
    instructions = models.JSONField()
    additional_notes = models.TextField(blank=True, null=True)
    servings = models.IntegerField(blank=True, null=True)
    image_url = models.URLField(max_length=2083, blank=True, null=True)
    website = models.URLField(max_length=2083, blank=True, null=True)
    mealType = models.CharField(max_length=50, choices=MEAL_TYPE_CHOICES, default='Dinner')
    categories = models.ManyToManyField(Category, related_name="recipes")
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recipe', 'category')