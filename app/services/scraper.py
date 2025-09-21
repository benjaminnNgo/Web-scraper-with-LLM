from abc import abstractmethod
from typing import Dict, Optional, Protocol

import requests

from app.constant import DESCRIPTION, ERROR, ERROR_MESSAGE_DETAIL
from app.services.html_process_hooks import (
    ExtractHTMLBodyHook,
    ExtractTextFromHTMLHook,
    HTMLProcessingHookManager,
)


class ScaperBase(Protocol):
    """Base class for web scaper."""

    @abstractmethod
    def __init__(self, url: str) -> None:
        """Initialize Scraper."""
        raise Exception('Need to be implemented for inheritance')

    @abstractmethod
    def get_url(self) -> Optional[str]:
        """Return url to webpage."""
        raise Exception('Need to be implemented for inheritance')

    @abstractmethod
    def scrap(self, content: str) -> Optional[Dict]:
        """Scrap the content of the website."""
        raise Exception('Need to be implemented for inheritance')


class CarDescriptionScraper(ScaperBase):
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
        html_processing_hm = HTMLProcessingHookManager()
        html_processing_hm.register(ExtractHTMLBodyHook())
        html_processing_hm.register(ExtractTextFromHTMLHook())

        content = html_processing_hm.execute(content)
        return {DESCRIPTION: content}


class ScraperBuilder:
    """Scraper information given url."""

    @classmethod
    def build(cls, scraper: ScaperBase) -> Optional[Dict]:
        target_url = scraper.get_url()

        try:
            response = requests.get(target_url)
            response.raise_for_status()
            content = response.text
            if len(content) == 0:
                return {DESCRIPTION: ''}
            else:
                return scraper.scrap(content)

        except requests.exceptions.RequestException as e:
            return {ERROR: f'Bad url:{scraper.get_url()}', ERROR_MESSAGE_DETAIL: str(e)}
