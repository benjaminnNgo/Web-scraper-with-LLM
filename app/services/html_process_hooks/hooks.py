from abc import abstractmethod
from typing import Protocol

from bs4 import BeautifulSoup


class HTMLProcessingHookBase(Protocol):
    """Base class for HTML processing hook."""

    @abstractmethod
    def __call__(self, input: str) -> str:
        """Perform HTML processing operation on the string."""
        raise Exception('Need to be implemented for inheritance')


class ExtractHTMLBodyHook(HTMLProcessingHookBase):
    """Hook to retrieve the body of HTML document."""

    def __call__(self, input: str) -> str:
        if input is None:
            raise ValueError("Can't perform str operation on None")
        soup = BeautifulSoup(input, 'html.parser')
        body_content = soup.body
        if body_content:
            return str(body_content)
        return ''


class ExtractTextFromHTMLHook(HTMLProcessingHookBase):
    """Hook to retrieve text only from HTML document."""

    def __call__(self, input: str) -> str:
        if input is None:
            raise ValueError("Can't perform str operation on None")

        soup = BeautifulSoup(input, 'html.parser')

        for script_or_style in soup(['script', 'style']):
            # We remove all HTML script and style HTML tag as all we need is text
            script_or_style.extract()
        cleaned_content = soup.get_text(separator='\n')
        cleaned_content = '\n'.join(  # remove empty space
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )
        return cleaned_content
