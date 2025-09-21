from typing import Dict
from unittest.mock import MagicMock, patch

import pytest

from app.constant import DESCRIPTION, ERROR, ERROR_MESSAGE_DETAIL
from app.services.scraper import CarDescriptionScraper, ScaperBase, ScraperBuilder


class DummyScraper(ScaperBase):
    """Dummy scraper for testing.

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


@pytest.fixture
def html_hook_factory():
    mock_hook = MagicMock()
    return mock_hook


@pytest.fixture
def html_process_hm_factory():
    mock_hm = MagicMock()
    mock_hm.execute.return_value = 'processed'
    return mock_hm

@pytest.fixture
def llm_wrapper_factory():
    mock_llm_wrapper = MagicMock()
    mock_llm_wrapper.prompt.return_value = "foo"
    return mock_llm_wrapper


@patch('app.services.scraper.ExtractHTMLBodyHook')
@patch('app.services.scraper.ExtractTextFromHTMLHook')
@patch('app.services.scraper.HTMLProcessingHookManager')
def test_CarDescriptionScraper_url(
    MockHTMLProcessingHookManager,
    MockExtractTextHook,
    MockExtractBodyHook,
    html_process_hm_factory,
    html_hook_factory,
):
    # Setup mocks
    MockHTMLProcessingHookManager.return_value = html_process_hm_factory
    MockExtractTextHook.return_value = html_hook_factory
    MockExtractBodyHook.return_value = html_hook_factory

    expected_url = 'https://foo'
    scraper = CarDescriptionScraper(expected_url)

    assert scraper.get_url() == expected_url

@patch('app.services.scraper.OllamaWrapper')
@patch('app.services.scraper.ExtractHTMLBodyHook')
@patch('app.services.scraper.ExtractTextFromHTMLHook')
@patch('app.services.scraper.HTMLProcessingHookManager')
def test_CarDescriptionScraper_output(
    MockHTMLProcessingHookManager,
    MockExtractTextHook,
    MockExtractBodyHook,
    MockOllamaWrapper,
    html_process_hm_factory,
    html_hook_factory,
    llm_wrapper_factory,
):
    # Setup mocks
    MockHTMLProcessingHookManager.return_value = html_process_hm_factory
    MockExtractTextHook.return_value = html_hook_factory
    MockExtractBodyHook.return_value = html_hook_factory
    MockOllamaWrapper.return_value = llm_wrapper_factory

    # Call the function
    scraper = CarDescriptionScraper('https://foo')
    output = scraper.scrap('raw html')

    # Assertions
    assert DESCRIPTION in output
    assert output == {DESCRIPTION: 'foo'}

    # Ensure hooks and manager were used correctly
    MockHTMLProcessingHookManager.assert_called_once()
    MockExtractTextHook.assert_called_once()
    MockExtractBodyHook.assert_called_once()
    html_process_hm_factory.register.assert_any_call(html_hook_factory)
    html_process_hm_factory.execute.assert_called_once_with('raw html')
    MockOllamaWrapper.assert_called_once()
    llm_wrapper_factory.prompt.assert_called_once_with('processed',scraper._get_template(),parse_description = scraper._get_task())


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
