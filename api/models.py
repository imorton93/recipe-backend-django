from django.db import models

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.JSONField()
    instructions = models.JSONField()
    additional_notes = models.TextField(blank=True, null=True)
    servings = models.IntegerField(blank=True, null=True)
    image_url = models.URLField(max_length=2083, blank=True, null=True)
    website = models.URLField(max_length=2083, blank=True, null=True)

    def __str__(self):
        return self.name