# LLM for web scraper

<div align="center">

[![Unit Tests](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/testing.yml/badge.svg?branch=main)](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/testing.yml)
[![Linting](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/ruff.yml/badge.svg?branch=main)](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/ruff.yml)

[![Docker Build](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/docker-build.yml/badge.svg?branch=main)](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/docker-build.yml)
[![Mypy Type Checking](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/mypy.yml/badge.svg?branch=main)](https://github.com/benjaminnNgo/LLM-challenge/actions/workflows/mypy.yml)

</div>

- [Overview](#overview)
- [Features and Tooling](#key-features-and-tooling)
- [Installation](#installation)

## Overview

This github repository provides implementation of web scrapper using any pre-train open-source LLM from [Ollama](https://github.com/ollama/ollama).

## Key Features and Tooling

This project is building with help of tools:

- :white_check_mark: [uv](https://docs.astral.sh/uv/)
- :white_check_mark: [unit test](tests/)
- :white_check_mark: CI support tool: Github Action
- :white_check_mark: [Open-source pre-train LLM model from Ollama](https://github.com/ollama/ollama)
- :white_check_mark: FastAPI
- :white_check_mark: Docker

Key features:

- :white_check_mark: Use open-source LLM to parse car description from any website.(for further information please visit document [here](docs/features.md#parse-car-description-from-vdp-url))

Due to time and resource constraint, the following features are left as future works:

- :white_large_square: Integration test
- :white_large_square: LLM inference on GPU(s) (since I don't have GPU machine/cluster available to explore this at this point)

Interesting future direction:

- :white_large_square: Parse customer reviews and ratings to learn demand and market trend
- :white_large_square: Parse promotions and incentives, which can help car dealer to learn marketing and sales strategy of opponent dealer

## Installation

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
docker run -p 8000:8000 -e LLM_MODEL_NAME=gemma3:1b -e OLLAMA_HOST=11434 --network llm_scraper_host llm-scraper-app
```

The app will be available at `http://127.0.0.1:8000/`.

To learn about available features and how to use them, please see [Features.md](docs/features.md)
