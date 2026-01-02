from typing import List
from .base import BasedLLMWrapper
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()


class GeminiWrapper(BasedLLMWrapper):
    """Provide Wrapper to prompt Gemini Google.

    Args:
        model (str): name of support Gemini model
    """

    def __init__(self, model='gemini-2.5-pro', temp=0.2):
        super().__init__()

        try:
            self.model = ChatGoogleGenerativeAI(
                model=model, convert_system_message_to_human=True, temperature=temp
            )
        except Exception:
            raise BrokenPipeError(
                'Fail to load Gemini model. Please Investigate.'  # @TODO: handle the error and throw proper error for user and logging to the system
            )

    def prompt(self, content: str, template: str, **kwargs) -> str:
        """Prompt to LLM given input and template."""
        batches_content = self.content_into_batch(content)
        parsed_results = []

        for i, chunk in enumerate(batches_content, start=0):
            response = self.model.invoke(
                [SystemMessage(content=template), HumanMessage(content=chunk)]
            )
            parsed_results.append(response.content)

        return '\n'.join(parsed_results)

    @classmethod
    def get_supporting_models(cls) -> List[str]:
        return [  # Free of charge model
            'gemini-2.5-pro',
            'gemini-2.5-flash',
            'gemini-2.5-flash-lite',
            'gemini-2.0-flash',
        ]

    @classmethod
    def system_init_check(cls, model, temp=0.2) -> None:
        # First check if the model name is valid
        if not model in GeminiWrapper.get_supporting_models():
            raise ValueError(f'Gemini model: {model} is not supported.')

        try:
            ChatGoogleGenerativeAI(
                model=model, convert_system_message_to_human=True, temperature=temp
            )
        except Exception as e:
            raise BrokenPipeError(f'Fail to load Gemini model. Please Investigate. {e}')
