from django.urls import resolve, reverse

from recipes.tests.test_recipe_base import RecipeTestBase
from recipes.views import site


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, site.RecipeDetail)

    def test_recipe_detail_view_returns_404_if_no_recipe_was_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1_000_000_000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_does_not_load_unpublished_recipes(self):
        recipe = self.create_recipe(is_published=False)
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': recipe.id}))  # type: ignore
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_correct_recipe(self):
        title = 'This is a detail recipe page that loads one recipe.'
        self.create_recipe(title=title)
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': 1}))
        content = response.content.decode('utf-8')
        self.assertIn(title, content)
