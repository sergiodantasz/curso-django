from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse(
            'recipes:category',
            kwargs={'category_id': 1}
        ))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse(
            'recipes:recipe',
            kwargs={'id': 1}
        ))
        self.assertIs(view.func, views.recipe)

    def test_recipe_home_view_returns_200(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_category_view_returns_404_if_no_recipe_was_found(self):
        response = self.client.get(reverse(
            'recipes:category',
            kwargs={'category_id': 1_000_000_000}
        ))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_returns_404_if_no_recipe_was_found(self):
        response = self.client.get(reverse(
            'recipes:recipe',
            kwargs={'id': 1_000_000_000}
        ))
        self.assertEqual(response.status_code, 404)

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

    def test_recipe_category_template_does_not_load_unpublished_recipes(self):
        recipe = self.create_recipe(is_published=False)
        response = self.client.get(reverse(
            'recipes:category',
            kwargs={'category_id': recipe.category.id}
        ))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_does_not_load_unpublished_recipes(self):
        recipe = self.create_recipe(is_published=False)
        response = self.client.get(reverse(
            'recipes:recipe',
            kwargs={'id': recipe.id}
        ))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        title = 'This is a category test.'
        self.create_recipe(title=title)
        response = self.client.get(reverse(
            'recipes:category',
            kwargs={'category_id': 1}
        ))
        content = response.content.decode('utf-8')
        self.assertIn(title, content)

    def test_recipe_detail_template_correct_recipe(self):
        title = 'This is a detail recipe page that loads one recipe.'
        self.create_recipe(title=title)
        response = self.client.get(reverse(
            'recipes:recipe',
            kwargs={'id': 1}
        ))
        content = response.content.decode('utf-8')
        self.assertIn(title, content)

    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search') + '?q=test'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=test'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;test&quot;',
            response.content.decode('utf-8')
        )
