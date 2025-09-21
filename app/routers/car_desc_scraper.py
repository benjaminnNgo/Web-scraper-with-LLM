from fastapi import APIRouter

from app.services import CarDescriptionScraper, ScraperBuilder

scraper_router = APIRouter()


@scraper_router.get('/')
def scraper(url: str):
    scraper = CarDescriptionScraper(url)
    result = ScraperBuilder.build(scraper)
    return result
