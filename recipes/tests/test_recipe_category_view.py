from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_returns_404_if_no_recipe_was_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1_000_000_000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_does_not_load_unpublished_recipes(self):
        recipe = self.create_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': recipe.category.id})  # type: ignore
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        title = 'This is a category test.'
        self.create_recipe(title=title)
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        content = response.content.decode('utf-8')
        self.assertIn(title, content)
