from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


@api_view(http_method_names=['GET'])
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()[:10]  # type: ignore
    serializer = RecipeSerializer(
        instance=recipes, many=True, context={'request': request}
    )
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)  # type: ignore
    serializer = RecipeSerializer(instance=recipe, context={'request': request})
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)  # type: ignore
    serializer = TagSerializer(instance=tag, context={'request': request})
    return Response(serializer.data)
