from fastapi import APIRouter

from app.services import CarDescriptionScraper, ScraperBuilder
from app.llm_models import OllamaWrapper, GeminiWrapper
from app.constant import (
    OLLAMA_MODEL_NAME,
    GEMINI_MODEL_NAME,
    OLLAMA_HOST,
)


scraper_router = APIRouter()


@scraper_router.get('/ollama')
def scraper(url: str):
    model = OllamaWrapper(
        model=OLLAMA_MODEL_NAME, base_url=f'http://ollama:{OLLAMA_HOST}'
    )
    scraper = CarDescriptionScraper(url, model)
    result = ScraperBuilder.build(scraper)
    return result


@scraper_router.get('/gemini')
def scraper(url: str):
    model = GeminiWrapper(GEMINI_MODEL_NAME)
    scraper = CarDescriptionScraper(url, model)
    result = ScraperBuilder.build(scraper)
    return result
