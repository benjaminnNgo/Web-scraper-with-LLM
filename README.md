# LLM for web scraper

<div align="center">

[![Unit Tests](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/testing.yml/badge.svg)](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/testing.yml)
[![Linting](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/ruff.yml/badge.svg)](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/ruff.yml)

[![Docker Build](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/docker-build.yml/badge.svg)](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/docker-build.yml)
[![Mypy Type Checking](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/mypy.yml/badge.svg)](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/mypy.yml)

</div>

# Instruction

To build and run my app. Docker is all you need! Please follows steps below:

1. Create a shared network for 2 `Docker` containers to communicate

```
docker network create llm_scraper_host
```

2. Build docker for `Ollama` at host `11434`

```
docker run --network llm_scraper_host -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

3. Execute `Ollama` model

```
docker exec -it ollama ollama run gemma3:1b
```

*Since I am building this app just using `cpu`, a lightweight model, `gemma3:1b`, is selected due to resource constraint.*

4. Build LLM web scraper app docker by using image as follows

```
docker build -t llm-scraper-app .
```

2. Then run docker

```
docker run -p 8000:8000 -e LLM_MODEL_NAME=gemma3:1b -e OLLAMA_HOST=11434 llm-scraper-app
```

The app will be available at `http://127.0.0.1:8000/`. To parse car description, you need use the endpoint at `/scraper` as follows:

```
http://127.0.0.1:8000/scraper/?url=replace_this_with_your_url
```
