from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse

@api_view(['GET', 'POST'])
def recipe_view(request):
    if request.method == 'GET':
        return Response({"message": "List of recipes"}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        return Response({"message": "Recipe created", "data": data}, status=status.HTTP_201_CREATED)
    

from recipe_scrapers import scrape_html
from requests.exceptions import RequestException
from urllib.request import urlopen
import requests

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