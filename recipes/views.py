from os import getenv

from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
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
        qs = qs.select_related('author', 'category')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, ctx.get('recipes'), PER_PAGE
        )
        ctx.update(
            {
                'recipes': page_obj,
                'pagination_range': pagination_range,
            }
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeAPI(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data().get('recipes').object_list.values()  # type: ignore
        return JsonResponse(list(recipes), safe=False)


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
        ctx.update({'title': f'{self.get_queryset()[0].category.name} | Category'})
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self):
        qs = super().get_queryset()
        search_term = self.request.GET.get('q')
        if not search_term:
            raise Http404()
        qs = qs.filter(
            Q(Q(title__icontains=search_term) | Q(description__icontains=search_term)),
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
        ctx.update({'is_detail_page': True})
        return ctx


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)
        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)
        if recipe_dict.get('cover'):
            recipe_dict['cover'] = (
                self.request.build_absolute_uri() + recipe_dict['cover'].url[1:]
            )
        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']
        return JsonResponse(recipe_dict, safe=False)
