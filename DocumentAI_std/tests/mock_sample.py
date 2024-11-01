import os

import easyocr
import numpy as np
import pytesseract
import pytest
import requests
from PIL import Image
from paddleocr import PaddleOCR

from DocumentAI_std.base.doc_element import DocElement
from DocumentAI_std.base.doc_element_classification import DocElementClassification
from DocumentAI_std.base.doc_enum import (
    ContentType,
    HorizontalAlignment,
    VerticalAlignment,
)
from DocumentAI_std.base.document import Document
from DocumentAI_std.base.document_entity_classification import (
    DocumentEntityClassification,
)


# FIXME: TO Install paddle ocr try: pip install "paddleocr>=2.0.1" --upgrade PyMuPDF==1.21.1


@pytest.fixture
def mock_doc_element():
    return DocElement(
        x=1, y=2, w=3, h=4, content_type=ContentType.TEXT, content="Mock Content"
    )


def mock_zip_codes():
    """Fixture providing a mix of valid and invalid ZIP code examples."""
    return [
        ("A1A 1A1", True),  # Valid Canadian postal code
        ("80001", True),  # Valid Canadian postal code
        ("80001-2222", True),  # Valid Canadian postal code
        ("800010", True),  # Valid Canadian postal code
        ("K1A0B1", True),  # Valid Canadian postal code without spaces
        ("M5V-2T6", False),  # Invalid format due to special character
        ("123 456", False),  # Invalid numeric ZIP code for Canada format
        ("A1A1A", False),  # Too short for Canadian format
        ("", False),  # Empty string
        (" ", False),  # Whitespace only
        ("1234 AB", False),  # Not a valid Canadian format
        ("B3H 2Y4", True),  # Another valid Canadian postal code with space
    ]

def mock_cities():
    return [
        ("New York", True),  # Known city
        ("mlkmml", False),  # Unknown city
        ("London", True),  # Known city
        ("bugsHugs", False),  # Unknown city
        ("Sousse", True),  # Known city
        ("Susah", True),  # Known city
        ("Debcha", False),  # Known city
    ]

def mock_person_names():
    return [
        ("John Doe", True, 1.0),      # Known person, 100% probability
        ("mlkmml", False, 0.0),       # Unknown entity, 0% probability
        ("Alice Johnson", True, 1.0), # Known person, 100% probability
        ("bugsHugs", False, 0.0),     # Not a person, 0% probability
        ("Michael Scott", True, 1.0), # Known person, 100% probability
        ("RandomCity", False, 0.0),   # Known city but not a person, 0% probability
        ("Steve", True, 1.0),         # Single name, detected as person
    ]
def mock_countries():
    return [
        ("United States", True),  # Known country name
        ("us", True),  # Known country code
        ("Canada", True),  # Known country name
        ("ca", True),  # Known country code
        ("Atlantis", False),  # Unknown country
        ("xyz", False),  # Unknown code
        ("France", True),  # Known country name
        ("fr", True),  # Known country code
        ("UnknownLand", False),  # Unknown country
    ]


@pytest.fixture
def mock_dates():
    return [
        "WHATEVER 22/10/2029 WHATEVER",
        "24 November 2008",
        "text 24/02/2021 ... 24-02-2021 ... 24_02_2021 ... 24|02|2021 text",
        "Monastir le 23 Avril 2020",
        "March 12, 2023",
        "12 March 2023",
        "03-12-2023",
        "03/12/2023",
        "XXXXXXXXXXX 03/12/2023 XXXXXXXX",
        "Monday 15 July 2023",
        "20/06/2023",
        "12/24/1998",
        "10-10-2020",
        "Grenade 02/01/1492",
    ]


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


def mock_ocr():
    return [
        ("paddle", ["fr"], "dummy_data/invoice.png"),
        ("tesseract", ["fr", "en"], "dummy_data/invoice.png"),
        ("easy", ["fr", "en"], "dummy_data/invoice.png"),
    ]


def mock_levenshtien():
    return [
        ("kitten", "sitting", 3),
        ("rosettacode", "raisethysword", 8),
        ("saturday", "sunday", 3),
        ("k", "kitten", 5),
        ("kitten", "k", 5),
        ("", "kitten", 6),
        ("kitten", "", 6),
        ("", "", 0),
        ("abcd", "abcd", 0),
        ("abc", "xyz", 3),
    ]


def mock_distances():
    return [
        (0, 0, 3, 4, 5, 7, 4),
        (1, 1, 4, 5, 5, 7, 4),
        (-1, -1, 2, 3, 5, 7, 4),
    ]


def mock_overlap():
    return [
        (
            DocElement(0, 0, 3, 3, ContentType.TEXT, "A"),
            DocElement(2, 2, 3, 3, ContentType.TEXT, "B"),
            0.1111111111111111,
        ),
        (
            DocElement(0, 0, 3, 3, ContentType.TEXT, "A"),
            DocElement(1, 1, 3, 3, ContentType.TEXT, "B"),
            0.4444444444444444,
        ),
        (
            DocElement(0, 0, 3, 3, ContentType.TEXT, "A"),
            DocElement(0, 0, 3, 3, ContentType.TEXT, "B"),
            1.0,
        ),
        (
            DocElement(0, 0, 3, 3, ContentType.TEXT, "A"),
            DocElement(4, 4, 3, 3, ContentType.TEXT, "B"),
            0.0,
        ),
    ]


def mock_horizontal_alignment():
    return [
        (
            DocElement(0, 0, 3, 3, ContentType.TEXT, "A"),
            DocElement(2, 2, 3, 3, ContentType.TEXT, "B"),
            HorizontalAlignment.LEFT,
        ),
        (
            DocElement(0, 0, 3, 3, ContentType.TEXT, "A"),
            DocElement(1, 1, 3, 3, ContentType.TEXT, "B"),
            HorizontalAlignment.LEFT,
        ),
        (
            DocElement(0, 0, 3, 3, ContentType.TEXT, "A"),
            DocElement(0, 0, 3, 3, ContentType.TEXT, "B"),
            HorizontalAlignment.CENTER,
        ),
        (
            DocElement(4, 4, 3, 3, ContentType.TEXT, "A"),
            DocElement(0, 0, 3, 3, ContentType.TEXT, "B"),
            HorizontalAlignment.RIGHT,
        ),
    ]


def mock_vertical_alignment():
    return [
        (
            DocElement(0, 0, 3, 3, ContentType.TEXT, "A"),
            DocElement(2, 2, 3, 3, ContentType.TEXT, "B"),
            VerticalAlignment.TOP,
        ),
        (
            DocElement(0, 0, 3, 3, ContentType.TEXT, "A"),
            DocElement(1, 1, 3, 3, ContentType.TEXT, "B"),
            VerticalAlignment.TOP,
        ),
        (
            DocElement(0, 0, 3, 3, ContentType.TEXT, "A"),
            DocElement(0, 0, 3, 3, ContentType.TEXT, "B"),
            VerticalAlignment.MIDDLE,
        ),
        (
            DocElement(0, 0, 3, 3, ContentType.TEXT, "A"),
            DocElement(4, 4, 3, 3, ContentType.TEXT, "B"),
            VerticalAlignment.TOP,
        ),
    ]


def mock_entropy():
    img_dir = os.path.join("dummy_data", "test")
    os.makedirs(img_dir, exist_ok=True)
    img_path = os.path.join(img_dir, "test.jpg")
    create_dummy_image(img_path)  # Create dummy image at the specified path
    return [
        (
            DocElement(0, 0, 10, 20, ContentType.TEXT, "A", "dummy_data/test/test.jpg"),
            dummy_entropy(
                DocElement(
                    0, 0, 10, 20, ContentType.TEXT, "A", "dummy_data/test/test.jpg"
                )
                .extract_pixels()
                .numpy()
            ),
        ),
        (
            DocElement(
                10, 0, 10, 15, ContentType.TEXT, "A", "dummy_data/test/test.jpg"
            ),
            dummy_entropy(
                DocElement(
                    10, 0, 10, 15, ContentType.TEXT, "A", "dummy_data/test/test.jpg"
                )
                .extract_pixels()
                .numpy()
            ),
        ),
        (
            DocElement(
                0, 60, 10, 20, ContentType.TEXT, "A", "dummy_data/test/test.jpg"
            ),
            dummy_entropy(
                DocElement(
                    0, 60, 10, 20, ContentType.TEXT, "A", "dummy_data/test/test.jpg"
                )
                .extract_pixels()
                .numpy()
            ),
        ),
    ]


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

    document = DocumentEntityClassification(img_path, ocr_output)

    return document


@pytest.fixture
def mock_paddle():
    mock_invoice()
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
    mock_invoice()
    reader = easyocr.Reader(
        ["en", "fr"]
    )  # this needs to run only once to load the model into memory
    result = reader.readtext("dummy_data/invoice.png")
    return result


@pytest.fixture
def mock_tesseract():
    mock_invoice()
    im = Image.open("dummy_data/invoice.png")
    im = im.convert("RGB")

    result = pytesseract.image_to_data(im, output_type=pytesseract.Output.DICT)

    return result


def create_dummy_image(file_path):
    # Create a dummy image with a white background
    image = Image.new("RGB", (200, 200), "white")
    # Save the image to the specified file path
    image.save(file_path)


def dummy_entropy(a):
    """
    This function calculates Shannon Entropy of an image
    For more information about the Entropy this link:
    https://en.wikipedia.org/wiki/Entropy_(information_theory)

    Parameters:
        input: 2d ndarray to process.

    Returns:
        entropy: float rounded to 4 decimal places

    Notes:
        The logarithm used is the bit logarithm (base-2).

    Examples:
        >>> import numpy as np
        >>> a = np.random.randint(0, 4095, (512,512))
        >>> ent = dummy_entropy(a)
        >>> ent
        11.9883

    """
    histogram, bin_edges = np.histogram(
        a,
        bins=int(a.max()) - int(a.min()) + 1,
        range=(int(a.min()), int(a.max()) + 1),
    )
    probabilities = histogram / a.size
    probabilities = probabilities[probabilities != 0]

    return -np.sum(probabilities * np.log2(probabilities))


def mock_invoice():
    img_dir = os.path.join("dummy_data")
    os.makedirs(img_dir, exist_ok=True)

    invoice_path = os.path.join(img_dir, "invoice.png")

    if os.path.exists(invoice_path):
        print("Invoice already exists at:", invoice_path)
        return

    invoice_url = (
        "https://assets-global.website-files.com/609d5d3c4d120e9c52e52b07/6331dbe479349413d652cd20_invoice"
        "-lp-sample-click-to-edit-p-500.png"
    )

    try:
        response = requests.get(invoice_url)
        response.raise_for_status()  # Raise an error for bad response status codes

        with open(invoice_path, "wb") as f:
            f.write(response.content)

        print("Invoice downloaded successfully.")
        print("Saved at:", invoice_path)

    except requests.exceptions.RequestException as e:
        print("Error downloading the invoice:", e)
