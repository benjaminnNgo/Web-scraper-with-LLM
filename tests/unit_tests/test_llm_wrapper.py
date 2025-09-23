from app.llm_models import BasedLLMWrapper


def test_break_up_content():
    llm_wrapper = BasedLLMWrapper()
    batches = llm_wrapper.content_into_batch('foo', seq_len=1)
    assert len(batches) == 3
    assert batches[0] == 'f'
    assert batches[1] == batches[2] == 'o'
