import requests
from abc import abstractmethod
from typing import Dict, Optional, Protocol

from app.constant import (
    DESCRIPTION,
    ERROR,
    ERROR_MESSAGE_DETAIL,
    LLM_MODEL_NAME,
    OLLAMA_HOST,
)
from app.services.html_process_hooks import (
    ExtractHTMLBodyHook,
    ExtractTextFromHTMLHook,
    HTMLProcessingHookManager,
)
from app.llm_models import OllamaWrapper


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
        self.llm_model = OllamaWrapper(
            model=LLM_MODEL_NAME, base_url=f'http://ollama:{OLLAMA_HOST}'
        )

    def get_url(self) -> str:
        return self.url

    def _get_template(self) -> str:
        template = (
            'You are tasked with extracting specific information from the following text content: {content}. '
            'Please follow these instructions carefully: \n\n'
            '1. **Extract Information:** Only extract the information that directly matches the provided description:{parse_description}'
            '2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. '
            "3. **Empty Response:** If no information matches the description, return an empty string ('')."
            '4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text.'
        )
        return template

    def _get_task(self) -> str:
        return 'Parse description of the car. Then write a paragraph of parsed description.'

    def scrap(self, content: str) -> Dict:
        """Scap information about the car."""
        # HTML pre-process
        html_processing_hm = HTMLProcessingHookManager()
        html_processing_hm.register(ExtractHTMLBodyHook())
        html_processing_hm.register(ExtractTextFromHTMLHook())
        content = html_processing_hm.execute(content)

        task = self._get_task()
        template = self._get_template()
        output = self.llm_model.prompt(content, template, parse_description=task)
        return {DESCRIPTION: output}


class ScraperBuilder:
    """Scraper information given url."""

    @classmethod
    def build(cls, scraper: ScaperBase) -> Optional[Dict]:
        target_url = scraper.get_url()

        try:
            response = requests.get(target_url)  # type: ignore
            response.raise_for_status()
            content = response.text
            if len(content) == 0:
                return {DESCRIPTION: ''}
            else:
                return scraper.scrap(content)

        except requests.exceptions.RequestException as e:
            return {ERROR: f'Bad url:{scraper.get_url()}', ERROR_MESSAGE_DETAIL: str(e)}
