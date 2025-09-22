from abc import abstractmethod
from typing import List


class BasedLLMWrapper:
    @abstractmethod
    def prompt(self, content: str, template: str, **kwargs) -> str:
        """Prompt LLM given input str and template."""
        raise Exception('Child wrapper is require to implement this feature.')

    def content_into_batch(self, content: str, seq_len=6000) -> List[str]:
        """Break up content into batchs of str with requested sequence length."""
        batch = []
        for i in range(0, len(content), seq_len):
            batch.append(content[i : i + seq_len])
        return batch
