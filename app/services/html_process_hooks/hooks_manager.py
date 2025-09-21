from copy import deepcopy

from .hooks import HTMLProcessingHookBase


class HTMLProcessingHookManager:
    """Manages hooks (`HTMLProcessingHookBase`s).

    This class allows you to register hooks that process HTML  for LLM promting.
    `HTMLProcessingHookManager` will maintain a list of `HTMLProcessingHookBase`'s
    and execute them by registration order. The string output of the ith hook is input
    string for the (i+1)th hook.
    """

    def __init__(self):
        self.hooks = []

    def register(self, hook: HTMLProcessingHookBase) -> None:
        """Register `HTMLProcessingHookBase` as a processing step."""
        self.hooks.append(hook)

    def execute(self, input: str) -> str:
        """Execute HTML processing pipeline."""
        if input == None:
            raise ValueError("Can't execute on None")

        processed_text = deepcopy(input)
        for hook in self.hooks:
            curr_text = hook(processed_text)
            processed_text = curr_text
        return processed_text
