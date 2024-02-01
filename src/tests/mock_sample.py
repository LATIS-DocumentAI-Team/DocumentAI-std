import os

import pytest
from PIL import Image

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
        "content": ["Text 1", "Text 2", "Text 3"],
    }

    img_dir = os.path.join("dummy_data", "test")
    os.makedirs(img_dir, exist_ok=True)
    img_path = os.path.join(img_dir, "test.jpg")
    create_dummy_image(img_path)  # Create dummy image at the specified path

    document = Document(img_path, ocr_output)

    return document


def create_dummy_image(file_path):
    # Create a dummy image with a white background
    image = Image.new("RGB", (200, 200), "white")
    # Save the image to the specified file path
    image.save(file_path)
