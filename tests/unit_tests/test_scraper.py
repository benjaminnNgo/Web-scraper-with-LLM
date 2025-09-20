from typing import Dict

import pytest

from app.constant import DESCRIPTION, ERROR, ERROR_MESSAGE_DETAIL
from app.services.scraper import (CarDescriptionScraper, ScaperBase,
                                  ScraperBuilder)


class DummyScraper(ScaperBase):
    """Scraper to retrieve information about the car given URL to the website.

    Args:
        url (str): URL to website of a car

    """

    def __init__(self, url: str) -> None:
        if url is None:
            raise ValueError("URL provided can't be None")
        self.url = url

    def get_url(self) -> str:
        return self.url

    def scrap(self, content: str) -> Dict:
        return {DESCRIPTION: content}


def test_CarDescriptionScraper():
    expected_url = 'https://foo'
    scraper = CarDescriptionScraper(expected_url)

    assert scraper.get_url() == f'https://r.jina.ai/{expected_url}'
    assert DESCRIPTION in scraper.scrap(
        'foo content'
    )  # @TODO: when scraper fully implemented. Need to mock here


def test_bad_CarDescriptionScraper():
    with pytest.raises(ValueError):
        CarDescriptionScraper(None)


def test_ScraperBuilder():
    scraper = DummyScraper(
        'https://httpbin.org/status/200'
    )  # always request sucessfully
    result = ScraperBuilder.build(scraper)
    assert DESCRIPTION in result


def test_bad_ScraperBuilder():
    scraper = DummyScraper('https://httpbin.org/status/404')  # always failed request
    result = ScraperBuilder.build(scraper)
    assert ERROR in result and ERROR_MESSAGE_DETAIL in result
