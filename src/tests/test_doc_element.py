from src.base.content_type import ContentType
from src.tests.mock_sample import mock_doc_element

def test_doc_element(mock_doc_element):
    assert mock_doc_element.x == 1
    assert mock_doc_element.y == 2
    assert mock_doc_element.w == 3
    assert mock_doc_element.h == 4
    assert mock_doc_element.content_type == ContentType.TEXT
    assert mock_doc_element.content == "Mock Content"