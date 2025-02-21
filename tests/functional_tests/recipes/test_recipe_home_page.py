from unittest.mock import patch

from pytest import mark
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional_tests.recipes.base import RecipeBaseFunctionalTests


@mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTests):
    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipe was found. :(', body.text)

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_search_input_find_correct_recipes(self):
        recipes = self.create_recipe_in_batch()
        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()
        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Search for a recipe"]'
        )
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )

    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.create_recipe_in_batch()
        self.browser.get(self.live_server_url)
        page_2 = self.browser.find_element(By.XPATH, '//a[@aria-label="Go to page 2."]')
        page_2.click()
        self.assertEqual(len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2)
