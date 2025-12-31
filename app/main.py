from fastapi import FastAPI, Response

from .routers import scraper_router
from app.llm_models import GeminiWrapper, OllamaWrapper
from app.constant import (
    OLLAMA_MODEL_NAME,
    GEMINI_MODEL_NAME,
)


def _pre_ollama_check() -> None:
    if not OLLAMA_MODEL_NAME in OllamaWrapper.get_supporting_models():
        raise ValueError(f'Ollama model: {OLLAMA_MODEL_NAME} is not supported.')


def _pre_gemini_check() -> None:
    if not GEMINI_MODEL_NAME in GeminiWrapper.get_supporting_models():
        raise ValueError(f'Ollama model: {OLLAMA_MODEL_NAME} is not supported.')


def _startup() -> None:
    r"""Perform system check and fail building if prerequisites doesn't meet."""
    _pre_ollama_check()
    _pre_gemini_check()


def _shutdown() -> None:
    r"""Handle closing services and cleaning system before shutting down."""
    print('INFO: Nothing to clean up (For now).')


async def lifespan(app: FastAPI):
    r"""This function will:
    - Execute _startup() to perform prerequisite check before launch the app.
    - Fail if any of prerequisites doesn't meet.
    - Otherwise, yield -> start servicing API request.
    - When the app is terminated, _shutdown() will be called to clean up (if need).
    """
    _startup()
    yield
    _shutdown()


application = FastAPI(lifespan=lifespan)
application.include_router(scraper_router, prefix='/scraper', tags=['scraper'])


@application.get('/')
def main():
    # lifespan()
    return Response(content='Hello from llm-challenge!', media_type='text/plain')


if __name__ == '__main__':
    main()
