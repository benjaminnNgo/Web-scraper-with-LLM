import os
from typing import Final

DESCRIPTION: Final[str] = 'description'
"""Key defined for JSON for returning to client request
"""

ERROR: Final[str] = 'error'
"""Key defined for JSON for returning to client request when Exception is raised.
This key would contain high overview information about why a query is fail
"""

ERROR_MESSAGE_DETAIL: Final[str] = 'error_detail'
"""Key defined for JSON for returning to client request when Exception is raised.
This key would contain detail information about why a query is fail
"""

OLLAMA_MODEL_NAME: Final[str] = os.getenv('OLLAMA_MODEL_NAME', 'gemma3:1b')
"""The name of the model desire to used is defined by setting os env.
When deploy app with docker, this variable is defined with following flag:
`-e OLLAMA_MODEL_NAME=<name of the model>`
"""

OLLAMA_HOST: Final[str] = os.getenv('OLLAMA_HOST', '11434')
"""URL endpoint of ollama host.
When deploy app with docker, this variable is defined with following flag:
`-e LLM_MODEL_NAME=<name of the model>`
"""

GEMINI_MODEL_NAME: Final[str] = os.getenv('GEMINI_MODEL_NAME', 'gemini-2.5-pro')
"""The name of the model desire to used is defined by setting os env.
When deploy app with docker, this variable is defined with following flag:
`-e GEMINI_MODEL_NAME=<name of the model>`
"""
