"""Tests for the DataFromHTMLSnippet HTML parser."""

from record_convertor.field_convertors.base_convertor.base_convertor_helpers import (
    DataFromHTMLSnippet,
)


def test_simple_html():
    """A simple paragraph tag extracts the text content."""
    parser = DataFromHTMLSnippet()
    assert parser.to_list("<p>hello</p>") == ["hello"]


def test_multiple_elements():
    """Multiple tags produce a list with each text element."""
    parser = DataFromHTMLSnippet()
    assert parser.to_list("<p>a</p><p>b</p>") == ["a", "b"]


def test_nested_tags():
    """Nested tags extract the innermost text."""
    parser = DataFromHTMLSnippet()
    assert parser.to_list("<div><span>text</span></div>") == ["text"]


def test_whitespace_only_tags():
    """Tags containing only whitespace produce an empty list."""
    parser = DataFromHTMLSnippet()
    assert parser.to_list("<p>   </p><p>  \n  </p>") == []


def test_mixed_content():
    """Tags with a mix of text and whitespace return only stripped text."""
    parser = DataFromHTMLSnippet()
    assert parser.to_list("<p>  hello  </p><p>   </p><p>world</p>") == [
        "hello",
        "world",
    ]


def test_plain_text():
    """Plain text without HTML tags is returned as a single-element list."""
    parser = DataFromHTMLSnippet()
    assert parser.to_list("just text") == ["just text"]


def test_empty_string():
    """An empty string produces an empty list."""
    parser = DataFromHTMLSnippet()
    assert parser.to_list("") == []


def test_complex_html():
    """Complex HTML with multiple nesting levels extracts all text."""
    parser = DataFromHTMLSnippet()
    result = parser.to_list("<div><h1>Title</h1><p>First <b>bold</b> text</p></div>")
    assert result == ["Title", "First", "bold", "text"]
