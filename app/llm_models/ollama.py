from .base import BasedLLMWrapper
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from typing import List


class OllamaWrapper(BasedLLMWrapper):
    """Provide Wrapper to prompt Ollama model.

    If a base URL to model host is provide, this wrapper will communicate directly with the host for prompting.
    Otherwise, Ollama is needed to install in local machine. If using Ollama on local machine. Make sure to pull
    desire model using `ollama pull` (please see ollama documentation for further information).

    Args:
        model (str): name of support Ollama model
        base_url (str|None): if Ollama model is hosted. Provided base URL to it
    """

    def __init__(self, model='llama3.1', base_url: str | None = None):
        super().__init__()
        try:
            if base_url:
                self.model = OllamaLLM(model=model, base_url=base_url)
            else:
                self.model = OllamaLLM(model=model)

        except Exception:
            raise Exception(
                'Please ensure to download ollama and install request models (See Ollama doc for further information. Or provided valid base URL to Ollama model host).'
            )

    def prompt(self, content: str, template: str, **kwargs) -> str:
        """Prompt to LLM given input and template."""
        template += '{content}'

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.model

        if not 'content' in prompt.input_variables:
            raise KeyError(
                'Provided template need a placehold for variable named `content`'
            )

        batches_content = self.content_into_batch(content)
        parsed_results = []

        for i, chunk in enumerate(batches_content, start=1):
            response = chain.invoke({'content': chunk, **kwargs})
            parsed_results.append(response)

        return '\n'.join(parsed_results)

    @classmethod
    def get_supporting_models(cls) -> List[str]:
        return ['gemma3:1b']  # @TODO: Current ollama doens't expose API to fetch this.

    @classmethod
    def system_init_check(cls, model_name, base_url=None):
        # First check if the model name is valid
        if not model_name in OllamaWrapper.get_supporting_models():
            raise ValueError(f'Ollama model: {model_name} is not supported.')

        try:
            if base_url:
                OllamaLLM(model=model_name, base_url=base_url)
            else:
                OllamaLLM(model=model_name)
        except Exception as e:
            raise BrokenPipeError(f'Fail to load Ollama model. Please Investigate. {e}')
