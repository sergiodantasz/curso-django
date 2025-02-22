from unittest.mock import patch

from django.urls import reverse
from rest_framework import test

from recipes.tests.test_recipe_base import RecipeMixin


class RecipeAPIv2TestMixin(RecipeMixin):
    def get_recipe_list_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        return api_url

    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_list_reverse_url(reverse_result)
        response = self.client.get(api_url)  # type: ignore
        return response

    def get_auth_data(self, username='user', password='pass'):
        userdata = {
            'username': username,
            'password': password,
        }
        user = self.create_author(
            username=userdata.get('username'),  # type: ignore
            password=userdata.get('password'),  # type: ignore
        )
        response = self.client.post(  # type: ignore
            reverse('recipes:token_obtain_pair'), data={**userdata}
        )
        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user,
        }

    def get_recipe_raw_data(self):
        return {
            'title': 'This is the title',
            'description': 'This is the description',
            'preparation_time': 1,
            'preparation_time_unit': 'Minutes',
            'servings': '1',
            'servings_unit': 'Person',
            'preparation_steps': 'This is the preparation steps.',
        }

    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(response.status_code, 200)  # type: ignore


class RecipeAPIv2Test(test.APITestCase, RecipeAPIv2TestMixin):
    @patch('recipes.views.api.RecipeAPIv2ListPagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.create_recipe_in_batch(qty=wanted_number_of_recipes)

        response = self.client.get(reverse('recipes:recipes-api-list') + '?page=1')
        qty_of_loaded_recipes = len(response.data.get('results'))  # type: ignore

        self.assertEqual(wanted_number_of_recipes, qty_of_loaded_recipes)

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.create_recipe_in_batch(qty=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(len(response.data.get('results')), 1)

    @patch('recipes.views.api.RecipeAPIv2ListPagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_category_id(self):
        category_wanted = self.create_category(name='WANTED_CATEGORY')
        category_not_wanted = self.create_category(name='NOT_WANTED_CATEGORY')
        recipes = self.create_recipe_in_batch(qty=10)
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()
        recipes[0].category = category_not_wanted
        recipes[0].save()
        api_url = (
            reverse('recipes:recipes-api-list') + f'?category_id={category_wanted.id}'  # type: ignore
        )
        response = self.get_recipe_api_list(reverse_result=api_url)
        self.assertEqual(len(response.data.get('results')), 9)

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_list_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(response.status_code, 401)

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        response = self.client.post(
            self.get_recipe_list_reverse_url(),
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}',
        )
        self.assertEqual(response.status_code, 201)

    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        recipe = self.create_recipe()
        access_data = self.get_auth_data(username='test_patch')
        jwt_access_token = access_data.get('jwt_access_token')
        author = access_data.get('user')
        recipe.author = author
        recipe.save()
        wanted_new_title = f'The new title updated by {author.username}'  # type: ignore
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),  # type: ignore
            data={'title': wanted_new_title},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}',
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            response.data.get('title'),  # type: ignore
            wanted_new_title,
        )

    def test_recipe_api_list_logged_user_cant_update_a_recipe_owned_by_another_user(
        self,
    ):
        recipe = self.create_recipe()
        access_data = self.get_auth_data(username='test_patch')
        another_user = self.get_auth_data(username='cant_update')
        jwt_access_token_from_another_user = another_user.get('jwt_access_token')
        author = access_data.get('user')
        recipe.author = author
        recipe.save()
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),  # type: ignore
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token_from_another_user}',
        )
        self.assertEqual(
            response.status_code,
            403,
        )
