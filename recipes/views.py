from os import getenv

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import DetailView, ListView

from recipes import models
from utils.pagination import make_pagination

PER_PAGE = int(getenv('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = models.Recipe
    context_object_name = 'recipes'
    ordering = ['-id']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, ctx.get('recipes'), PER_PAGE)
        ctx.update(
            {
                'recipes': page_obj,
                'pagination_range': pagination_range,
            }
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(category__id=self.kwargs.get('category_id'))
        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update(
            {
                'title': f'{self.get_queryset()[0].category.name} | Category'
            }
        )
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self):
        qs = super().get_queryset()
        search_term = self.request.GET.get('q')
        if not search_term:
            raise Http404()
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q')
        ctx.update(
            {
                'title': f'Search for "{search_term}"',
                'search_term': search_term,
                'additional_url_query': f'&q={search_term}',
            }
        )
        return ctx


class RecipeDetail(DetailView):
    model = models.Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update(
            {
                'is_detail_page': True
            }
        )
        return ctx
