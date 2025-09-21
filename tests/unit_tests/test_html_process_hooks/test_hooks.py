import pytest

from app.services.html_process_hooks import ExtractHTMLBodyHook, ExtractTextFromHTMLHook


def test_extract_html_body_hook():
    empty_html = ''
    extract_html_body_hook = ExtractHTMLBodyHook()
    output = extract_html_body_hook(empty_html)
    assert output == empty_html

    content = """
<html>
  <head><title>Example</title></head>
  <body>
    <h1>Hello</h1>
    <p>This is inside the body.</p>
  </body>
</html>
    """
    output = extract_html_body_hook(content)
    expected = """<body>
<h1>Hello</h1>
<p>This is inside the body.</p>
</body>"""
    assert output == expected


def test_extract_text_hook():
    empty_html = ''
    extract_text_from_html_hook = ExtractTextFromHTMLHook()
    output = extract_text_from_html_hook(empty_html)
    assert output == empty_html

    content = """
<html>
  <head><title>Example</title></head>
  <body>
    <h1>Hello</h1>
    <p>This is inside the body.</p>
  </body>
</html>
    """
    output = extract_text_from_html_hook(content)
    expected = """Example
Hello
This is inside the body."""
    assert output == expected


def test_bad_extract_html_body_hook():
    extract_html_body_hook = ExtractHTMLBodyHook()
    with pytest.raises(ValueError):
        extract_html_body_hook(None)


def test_bad_extract_text_from_hook():
    extract_html_body_hook = ExtractTextFromHTMLHook()
    with pytest.raises(ValueError):
        extract_html_body_hook(None)
