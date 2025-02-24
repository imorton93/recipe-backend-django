from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.get_recipes, name='get_recipes'),
    path('recipes/<int:id>/', views.get_recipe, name='get_recipe'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/<int:id>/update/', views.update_recipe, name='update_recipe'),
    path('recipes/<int:id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('scrape-recipe/', views.scrape_recipe_view, name='scrape_recipe'),

    path('categories/', views.get_categories, name='get_folders'), 
    path('categories/<int:id>/', views.get_category, name='get_folder'), 
    path('categories/add/', views.add_category, name='add_folder'), 
    path('categories/<int:id>/update/', views.update_Category, name='update_folder'), 
    path('categories/<int:id>/delete/', views.delete_category, name='delete_folder'),

]