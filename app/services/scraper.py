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
            'You are an expert in the car industry. Your task is as follows:'
            'Given the following web page content:{content}'
            '\n\nPlease follow these instructions carefully:'
            '1. Carefully review the text and identify any {parse_description} (such as exterior style, technology, comfort, performance, safety, etc.)'
            "2.If you find any car features, extract a concise, high-quality description of the car, starting your response with:'A beautiful car with ...'(and then continue with the extracted features)"
            "3.If you do not find any car features, respond with an empty string ('')."
            '4.Do not include any additional text, comments, or explanations in your response.'
            '5.Only extract the information that are directly about {parse_description}.'
            '6.Output must be a plain string, with no markdown, no code fences, no language labels.'
        )

        return template

    def _get_task(self) -> str:
        return 'car features'

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
