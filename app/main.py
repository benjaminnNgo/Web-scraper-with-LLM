from fastapi import FastAPI, Response

from .routers import scraper_router

application = FastAPI()


@application.get('/')
def main():
    return Response(content='Hello from llm-challenge!', media_type='text/plain')

application.include_router(scraper_router, prefix='/scraper', tags=['scraper'])


if __name__ == '__main__':
    main()
