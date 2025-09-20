from fastapi import FastAPI, Response

application = FastAPI()


@application.get('/')
def main():
    return Response(content='Hello from llm-challenge!', media_type='text/plain')


if __name__ == '__main__':
    main()
