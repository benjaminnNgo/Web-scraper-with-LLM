from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import application
from app.services.scraper import CarDescriptionScraper


@pytest.fixture
def client():
    return TestClient(application)


@pytest.fixture
def scraper_factory():
    scraper_builder = MagicMock()
    scraper_builder.build


def test_main(client):
    response = client.get('/')
    assert response.status_code == 200
    assert len(response.text) > 0


@pytest.fixture
def scraper_builder_mock():
    with patch('app.services.scraper.ScraperBuilder.build') as mock_build:
        yield mock_build


def test_scraper(client, scraper_builder_mock):
    test_url = 'http://example.com/car'
    expected_result = {'description': 'mocked description'}
    scraper_builder_mock.return_value = expected_result

    response = client.get('/scraper', params={'url': test_url})

    scraper_builder_mock.assert_called_once()
    called_scraper = scraper_builder_mock.call_args[0][0]
    assert isinstance(called_scraper, CarDescriptionScraper)
    assert called_scraper.url == test_url
    assert response.status_code == 200
    assert response.json() == expected_result
