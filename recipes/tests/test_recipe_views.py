from django.test import TestCase
from django.urls import resolve, reverse

from recipes import models, views


class RecipeViewsTest(TestCase):
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
            '<h1>No recipe was found. :(</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        category = models.Category.objects.create(name='Categoria Teste')
        author = models.User.objects.create_user(
            first_name='Benedito',
            last_name='Barbosa',
            username='benedito',
            password='Benedito@123',
            email='beneditobarbosa@django.com'
        )
        recipe = models.Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='minutes',
            servings=5,
            servings_unit='portions',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True
        )
        response = self.client.get(reverse('recipes:home'))
        context_recipes = response.context.get('recipes')
        content = response.content.decode('utf-8')
        self.assertEqual(len(context_recipes), 1)
        self.assertIn('Recipe Title', content)
        self.assertIn('10 minutes', content)
        self.assertIn('Recipe Description', content)
        self.assertIn('5 portions', content)
