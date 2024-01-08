from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from utils.browser import make_edge_browser


class RecipeBaseFunctionalTests(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_edge_browser('--headless')
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
