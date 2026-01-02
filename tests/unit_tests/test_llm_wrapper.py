from unittest.mock import MagicMock, patch

from app.llm_models import BasedLLMWrapper, OllamaWrapper, GeminiWrapper
from langchain_core.messages import HumanMessage, SystemMessage
import pytest


def test_break_up_content():
    llm_wrapper = BasedLLMWrapper()
    batches = llm_wrapper.content_into_batch('foo', seq_len=1)
    assert len(batches) == 3
    assert batches[0] == 'f'
    assert batches[1] == batches[2] == 'o'


@patch('app.llm_models.ollama.OllamaLLM')
def test_ollama(mock_ollama_cls):
    expect_response = 'mocked response'
    mock_model_instance = MagicMock(return_value=expect_response)
    mock_ollama_cls.return_value = mock_model_instance

    model = OllamaWrapper()
    assert OllamaWrapper.get_supporting_models() == ['gemma3:1b']

    with patch.object(
        model, 'content_into_batch', return_value=['foo', 'content']
    ) as mock_batch:
        response = model.prompt(content='foo content', template='foo template:')
        assert response == f'{expect_response}\n{expect_response}'
        mock_batch.assert_called_once()
        assert mock_model_instance.call_count == 2


@patch('app.llm_models.gemini.ChatGoogleGenerativeAI')
def test_gemini(mock_gemini_cls):
    expect_response = 'mock response'
    response_mock = MagicMock()
    response_mock.content = expect_response
    invoke_mock = MagicMock(return_value=response_mock)
    mock_model_instance = MagicMock()
    mock_model_instance.invoke = invoke_mock
    mock_gemini_cls.return_value = mock_model_instance

    model = GeminiWrapper()
    assert GeminiWrapper.get_supporting_models() == [  # Free of charge model
        'gemini-2.5-pro',
        'gemini-2.5-flash',
        'gemini-2.5-flash-lite',
        'gemini-2.0-flash',
    ]

    with patch.object(
        model, 'content_into_batch', return_value=['foo', 'content']
    ) as mock_batch:
        response = model.prompt(content='foo content', template='foo template')
        assert response == f'{expect_response}\n{expect_response}'
        mock_batch.assert_called_once()
        invoke_mock.call_count == 2
        invoke_mock.assert_any_call(
            [SystemMessage(content='foo template'), HumanMessage(content='foo')]
        )
        invoke_mock.assert_any_call(
            [SystemMessage(content='foo template'), HumanMessage(content='content')]
        )


@patch('app.llm_models.gemini.ChatGoogleGenerativeAI')
def test_gemini_system_init_check(mock_gemini_cls, monkeypatch):
    mock_gemini_cls.side_effect = Exception('init failed')

    with pytest.raises(ValueError):
        GeminiWrapper.system_init_check('foo')

    monkeypatch.delenv('GEMINI_API_KEY', raising=False)
    with pytest.raises(BrokenPipeError):
        GeminiWrapper.system_init_check('gemini-2.5-pro')


@patch('app.llm_models.ollama.OllamaLLM')
def test_gemini_system_init_check(mock_ollama_cls, monkeypatch):
    mock_ollama_cls.side_effect = Exception('init failed')

    with pytest.raises(ValueError):
        OllamaWrapper.system_init_check('foo')

    with pytest.raises(BrokenPipeError):
        OllamaWrapper.system_init_check('gemma3:1b')

    with pytest.raises(BrokenPipeError):
        OllamaWrapper.system_init_check('gemma3:1b', 'foo_url')
