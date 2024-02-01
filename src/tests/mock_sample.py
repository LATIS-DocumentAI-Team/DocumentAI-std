import pytest

from src.base.content_type import ContentType
from src.base.doc_element_classification import DocElementClassification
from src.base.doc_element import DocElement
from src.base.document import Document


@pytest.fixture
def mock_doc_element():
    return DocElement(
        x=1, y=2, w=3, h=4, content_type=ContentType.TEXT, content="Mock Content"
    )


@pytest.fixture
def mock_doc_element_classification():
    return DocElementClassification(
        x=1,
        y=2,
        w=3,
        h=4,
        content_type=ContentType.TEXT,
        content="Mock Content",
        label=5,
    )


@pytest.fixture
def mock_document():
    # Dummy data for ocr_output
    ocr_output = {
        "bbox": [[10, 20, 30, 40], [50, 60, 70, 80], [90, 100, 110, 120]],
        "content": ["Text 1", "Text 2", "Text 3"]
    }

    img_path = "/path/to/your/image.jpg"
    document = Document(img_path, ocr_output)

    return document
