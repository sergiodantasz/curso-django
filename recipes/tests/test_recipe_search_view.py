from django.urls import resolve, reverse

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func.view_class, views.RecipeListViewSearch)

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

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one.'
        title2 = 'This is recipe two.'
        recipe1 = self.create_recipe(
            slug='recipe-one',
            title=title1,
            author_data={'username': 'UserOne'}
        )
        recipe2 = self.create_recipe(
            slug='recipe-two',
            title=title2,
            author_data={'username': 'UserTwo'}
        )
        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')
        self.assertIn(recipe1, response1.context.get('recipes'))
        self.assertNotIn(recipe2, response1.context.get('recipes'))
        self.assertIn(recipe2, response2.context.get('recipes'))
        self.assertNotIn(recipe1, response2.context.get('recipes'))
        self.assertIn(recipe1, response_both.context.get('recipes'))
        self.assertIn(recipe2, response_both.context.get('recipes'))
