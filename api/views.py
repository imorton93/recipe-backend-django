from django.shortcuts import render


# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from recipe_scrapers import scrape_html
from requests.exceptions import RequestException
from urllib.request import urlopen
import requests
from .serializers import RecipeSerializer, CategorySerializer
from .models import Recipe, Category
import logging
 
logger = logging.getLogger(__name__)


# Get all recipes 
@api_view(['GET'])
def get_recipes(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Get a single recipe
@api_view(['GET'])
def get_recipe(request, id):
    try:
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return Response({"message": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Add Recipe
@api_view(['POST'])
def add_recipe(request):
    category_ids = request.data.pop('categories', []) #get category IDs
    serializer = RecipeSerializer(data=request.data)
    if serializer.is_valid():
        recipe = serializer.save()
        recipe.categories.set(category_ids)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update recipe
@api_view(['PUT', 'PATCH'])
def update_recipe(request, id):
    try:
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return Response({"message": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
    # partial=True allows partial updates (PATCH)

    logger.debug(f"Received data: {request.data}")

    serializer = RecipeSerializer(recipe, data=request.data, partial=True)  
    if serializer.is_valid():
        
        logger.debug(f"Serializer data is valid, saving recipe with data: {serializer.validated_data}")
        serializer.save()

        category_ids = request.data.get('categories', [])
        logger.debug(f"Categories received: {category_ids}")

        try:
            categories = Category.objects.filter(id__in=category_ids)
            recipe.categories.set(categories)
            logger.debug(f"Categories updated successfully: {categories}")
        except Exception as e:
            logger.error(f"Error updating categories: {str(e)}")

        return Response(serializer.data, status=status.HTTP_200_OK)
    logger.error(f"Serializer errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Delete a Recipe
@api_view(['DELETE'])
def delete_recipe(request, id):
    try:
        recipe = Recipe.objects.get(id=id)
        recipe.delete()
        return Response({"message": "Recipe deleted"}, status=status.HTTP_204_NO_CONTENT)
    except Recipe.DoesNotExist:
        return Response({"message": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)



# Scrape recipe with given url
@api_view(['GET'])
def scrape_recipe_view(request):
    url = request.query_params.get('url')

    if not url:
        return Response({'error': 'URL parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        # html = urlopen(url).read().decode("utf-8")
        response = requests.get(url, headers=headers, timeout=10)
        # Raise and error for HTTP errors
        response.raise_for_status()
        # scraper = scrape_html(html, org_url=url)
        scraper = scrape_html(response.content, org_url=url)
        data = {
            'title': scraper.title(),
            'ingredients': scraper.ingredients(),
            'instructions': scraper.instructions(),
            'image': scraper.image(),  # Optional
            'host': scraper.host(),  # Optional (site name)
            'servings': scraper.yields(),
        }
        return Response(data, status=status.HTTP_200_OK)

    except RequestException as e:
        return Response({'error': f'Failed to fetch URL: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': f'Scraping failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# Get all categories
@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Get a single category
@api_view(['GET'])
def get_category(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"message": "category not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Add a new category
@api_view(['POST'])
def add_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update a category
@api_view(['PUT', 'PATCH'])
def update_Category(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"message": "category not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a category
@api_view(['DELETE'])
def delete_category(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return Response({"message": "category deleted"}, status=status.HTTP_204_NO_CONTENT)
    except Category.DoesNotExist:
        return Response({"message": "category not found"}, status=status.HTTP_404_NOT_FOUND)