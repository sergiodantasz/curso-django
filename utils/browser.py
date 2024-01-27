from pathlib import Path

from selenium import webdriver
from selenium.webdriver.edge.service import Service

ROOT_PATH = Path(__file__).parent.parent
EDGEDRIVER_NAME = 'msedgedriver'
EDGEDRIVER_PATH = ROOT_PATH / 'bin' / EDGEDRIVER_NAME


def make_edge_browser(*options):
    edge_options = webdriver.EdgeOptions()
    for option in options:
        edge_options.add_argument(option)
    edge_service = Service(str(EDGEDRIVER_PATH))
    browser = webdriver.Edge(edge_options, edge_service)
    return browser
