from django.shortcuts import render

from utils.recipes.factory import make_recipe

from . import models


def home(request):
    recipes = models.Recipe.objects.filter(is_published=True).order_by('-id')
    return render(
        request,
        'recipes/pages/home.html',
        {
            'recipes': recipes,
        }
    )


def recipe(request, id):
    return render(
        request,
        'recipes/pages/recipe.html',
        {
            'recipe': make_recipe(),
            'is_detail_page': True,
        }
    )


def category(request, category_id):
    recipes = models.Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id')
    return render(
        request,
        'recipes/pages/category.html',
        {
            'recipes': recipes,
        }
    )
