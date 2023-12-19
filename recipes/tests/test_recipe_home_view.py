from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_200(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipe_was_found_if_no_recipe_was_found(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipe was found. :(',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.create_recipe()
        response = self.client.get(reverse('recipes:home'))
        context_recipes = response.context.get('recipes')
        content = response.content.decode('utf-8')
        self.assertEqual(len(context_recipes), 1)
        self.assertIn('Recipe Title', content)

    def test_recipe_home_template_does_not_load_unpublished_recipes(self):
        self.create_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipe was found. :(',
            response.content.decode('utf-8')
        )

    def test_recipe_home_is_paginated(self):
        for i in range(8):
            kwargs = {
                'slug': f'r{i}',
                'author_data': {
                    'username': f'u{i}'
                }
            }
            self.create_recipe(**kwargs)
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context.get('recipes')
            paginator = recipes.paginator
            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.create_recipe(**kwargs)
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=1A')
            self.assertEqual(
                response.context['recipes'].number,
                1
            )
            response = self.client.get(reverse('recipes:home') + '?page=2')
            self.assertEqual(
                response.context['recipes'].number,
                2
            )
            response = self.client.get(reverse('recipes:home') + '?page=3')
            self.assertEqual(
                response.context['recipes'].number,
                3
            )
