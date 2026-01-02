from abc import abstractmethod
from typing import List


class BasedLLMWrapper:
    @abstractmethod
    def prompt(self, content: str, template: str, **kwargs) -> str:
        r"""Prompt LLM given input str and template."""
        raise NotImplementedError('Child wrapper is require to implement this feature.')

    def content_into_batch(self, content: str, seq_len=6000) -> List[str]:
        r"""Break up content into batchs of str with requested sequence length."""
        batch = []
        for i in range(0, len(content), seq_len):
            batch.append(content[i : i + seq_len])
        return batch

    @classmethod
    @abstractmethod
    def get_supporting_models(cls) -> List[str]:
        r"""Get list of available models."""
        raise NotImplementedError('Child wrapper is require to implement this feature.')

    @classmethod
    def system_init_check(cls, *args, **kwargs) -> None:
        r"""Perform init check. This method should be run before starting up the app."""
        raise NotImplementedError('Child wrapper is require to implement this feature.')
