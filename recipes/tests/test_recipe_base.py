from django.test import TestCase

from recipes import models


class RecipeTestBase(TestCase):
    @staticmethod
    def create_category(name: str = 'Category'):
        return models.Category.objects.create(name=name)

    @staticmethod
    def create_author(
        first_name: str = 'UserFirstName',
        last_name: str = 'UserLastName',
        username: str = 'username',
        email: str = 'username@django.com',
        password: str = '123'
    ):
        return models.User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email
        )

    def create_recipe(
        self,
        category_data: dict | None = None,
        author_data: dict | None = None,
        title: str = 'Recipe Title',
        description: str = 'Recipe Description',
        slug: str = 'recipe-slug',
        preparation_time: int | float = 10,
        preparation_time_unit: str = 'minutes',
        servings: int | float = 5,
        servings_unit: str = 'portions',
        preparation_steps: str = 'Recipe Preparation Steps',
        preparation_steps_is_html: bool = False,
        is_published: bool = True
    ):
        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}
        return models.Recipe.objects.create(
            category=self.create_category(**category_data),
            author=self.create_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published
        )
