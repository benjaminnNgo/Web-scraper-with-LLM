from typing import Dict, List
from unittest.mock import MagicMock, patch

import pytest

from app.constant import DESCRIPTION, ERROR, ERROR_MESSAGE_DETAIL
from app.services.scraper import CarDescriptionScraper, ScaperBase, ScraperBuilder,BasedLLMWrapper


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
        
class MockLLMWrapper(BasedLLMWrapper):
    last_content : str = ''
    last_template : str = ''
    prompt_call_count : int = 0
    def prompt(self, content: str, template: str, **kwargs) -> str:
        self.last_content = content
        self.last_template = template
        self.prompt_call_count += 1
        return "foo"
    
    def get_supporting_models(cls) -> List[str]:
        return ['foo-model']

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
    mock_llm_wrapper.prompt.return_value = 'foo'
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
    mockLLMWrapper = MockLLMWrapper()
    scraper = CarDescriptionScraper(expected_url,mockLLMWrapper)

    assert scraper.get_url() == expected_url


@patch('app.services.scraper.ExtractHTMLBodyHook')
@patch('app.services.scraper.ExtractTextFromHTMLHook')
@patch('app.services.scraper.HTMLProcessingHookManager')
def test_CarDescriptionScraper_output(
    MockHTMLProcessingHookManager,
    MockExtractTextHook,
    MockExtractBodyHook,
    html_process_hm_factory,
    html_hook_factory,
    llm_wrapper_factory,
):
    # Setup mocks
    MockHTMLProcessingHookManager.return_value = html_process_hm_factory
    MockExtractTextHook.return_value = html_hook_factory
    MockExtractBodyHook.return_value = html_hook_factory

    # Call the function
    mockLLMWrapper = MockLLMWrapper()
    scraper = CarDescriptionScraper('https://foo',mockLLMWrapper)
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
    assert mockLLMWrapper.prompt_call_count == 1
    assert mockLLMWrapper.last_content == 'processed'
    assert mockLLMWrapper.last_template == scraper._get_template()


def test_bad_CarDescriptionScraper():
    mockLLMWrapper = MockLLMWrapper()
    with pytest.raises(ValueError):
        CarDescriptionScraper(None,mockLLMWrapper)

    with pytest.raises(ValueError):
        CarDescriptionScraper("foo",None)
    


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
