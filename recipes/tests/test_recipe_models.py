from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from parameterized import parameterized

from recipes import models
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeRecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.create_recipe()
        return super().setUp()
    
    def create_recipe_without_defaults(self):
        recipe = models.Recipe(
            category=self.create_category('Test Default Category'),
            author=User.objects.create_user(
                username='UserTest',
                first_name='UserFirstName',
                last_name='UserLastName',
                email='usertest@django.com',
                password='999'
            ),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='minutes',
            servings=5,
            servings_unit='portions',
            preparation_steps='Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand(
        [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 20),
            ('servings_unit', 20),
        ]
    )
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, '*' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.create_recipe_without_defaults()
        self.assertFalse(recipe.preparation_steps_is_html)

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.create_recipe_without_defaults()
        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing Representation')


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.create_category('Category Testing')
        return super().setUp()

    def test_category_string_representation(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_category_name_field_max_length_is_more_than_65_chars(self):
        self.category.name = '*' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
