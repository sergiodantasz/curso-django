from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from recipes.tests.test_recipe_base import RecipeMixin
from utils.browser import make_edge_browser


class RecipeBaseFunctionalTests(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_edge_browser('--headless')
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
