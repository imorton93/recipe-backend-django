from rest_framework import serializers
from .models import Recipe, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'ingredients', 'instructions', 'mealType', 'additional_notes', 'servings', 'image_url', 'website', 'categories', 'favorite']