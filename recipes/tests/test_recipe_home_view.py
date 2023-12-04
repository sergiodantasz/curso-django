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