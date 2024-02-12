import logging
import os

import easyocr
import pytesseract
import pytest
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR

# FIXME: TO Install paddle ocr try: pip install "paddleocr>=2.0.1" --upgrade PyMuPDF==1.21.1
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


@pytest.fixture
def mock_document_entity_classification():
    # Dummy data for ocr_output
    ocr_output = {
        "bbox": [[10, 20, 30, 40], [50, 60, 70, 80], [90, 100, 110, 120]],
        "content": ["Text 1", "Text 2", "Text 3"],
        "label": [1, 1, 2],
    }

    img_dir = os.path.join("dummy_data", "test")
    os.makedirs(img_dir, exist_ok=True)
    img_path = os.path.join(img_dir, "test.jpg")
    create_dummy_image(img_path)  # Create dummy image at the specified path

    document = Document(img_path, ocr_output)

    return document


@pytest.fixture
def mock_paddle():
    im = Image.open("dummy_data/invoice.png")
    im = im.convert("RGB")

    ocr = PaddleOCR(
        use_angle_cls=True,
        max_text_length=2,
        use_space_char=True,
        lang="french",
        type="structure",
    )
    result = ocr.ocr(np.asarray(im), cls=True)

    return result


@pytest.fixture
def mock_easy():
    reader = easyocr.Reader(
        ["en", "fr"]
    )  # this needs to run only once to load the model into memory
    result = reader.readtext("dummy_data/invoice.png")
    return result


@pytest.fixture
def mock_tesseract():
    im = Image.open("dummy_data/invoice.png")
    im = im.convert("RGB")

    result = pytesseract.image_to_data(im, output_type=pytesseract.Output.DICT)

    return result


def create_dummy_image(file_path):
    # Create a dummy image with a white background
    image = Image.new("RGB", (200, 200), "white")
    # Save the image to the specified file path
    image.save(file_path)
