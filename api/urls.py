from django.urls import path
from .views import recipe_view, scrape_recipe_view 

urlpatterns = [
    path('recipes/', recipe_view),
    path('scrape-recipe/', scrape_recipe_view),
]