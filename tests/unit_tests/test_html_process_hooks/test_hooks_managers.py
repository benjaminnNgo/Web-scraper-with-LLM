import pytest

from app.services.html_process_hooks import (
    HTMLProcessingHookBase,
    HTMLProcessingHookManager,
)


class MockHook(HTMLProcessingHookBase):
    """MockHook for testing HookManager."""

    def __init__(self, id: str):
        self.id = id
        self.count = {'call_count': 0}

    def __call__(self, input: str) -> str:
        """Simple str transformation: just concate Hook id to the end of input str."""
        self.count['call_count'] += 1
        return f'{input}{self.id}'


def test_html_processing_hm():
    begin_str = 'foo'
    hm = HTMLProcessingHookManager()
    final_str = hm.execute(begin_str)

    # No hook register yet. No str transformation expected
    assert final_str == begin_str

    hook1 = MockHook('a')
    hook2 = MockHook('b')
    hm.register(hook1)
    hm.register(hook2)
    final_str = hm.execute(begin_str)

    assert final_str == 'fooab'


def test_bad_html_processing_hm():
    hm = HTMLProcessingHookManager()
    hook1 = MockHook('a')
    hook2 = MockHook('b')
    hm.register(hook1)
    hm.register(hook2)

    with pytest.raises(ValueError):
        hm.execute(None)
