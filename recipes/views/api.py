from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


@api_view(http_method_names=['GET', 'POST'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]  # type: ignore
        serializer = RecipeSerializer(
            instance=recipes, many=True, context={'request': request}
        )
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = RecipeSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['GET', 'PATCH', 'DELETE'])
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)  # type: ignore
    if request.method == 'GET':
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request': request},
        )
        return Response(serializer.data)
    if request.method == 'PATCH':
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )
    if request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET'])
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)  # type: ignore
    serializer = TagSerializer(instance=tag, context={'request': request})
    return Response(serializer.data)
