# DocumentAI-std

**DocumentAI-std** is a Python library crafted for streamlined and standardized document analysis, with a particular focus on tasks like document element processing, optical character recognition (OCR), and dataset management for key information extraction. Designed for ease of use and flexibility, it provides tools to work with Visually Rich Documents (VRDs) and supports datasets like Wildreceipt, XFUND, FUNSD, and CORD. Whether you're working on research or developing production systems, **DocumentAI-std** simplifies document processing workflows.

## Features

- **Visually Rich Document Object Model (VRDOM)**: A framework for representing document content through structured elements with bounding boxes and content types.
- **Support for OCR**: Seamlessly integrate OCR results to create a structured document representation.
- **Document Dataset Handling**: Utilities for managing datasets like **Wildreceipt**, including loading, annotation, and validation.

## Installation

You can install **DocumentAI-std** using the following command:

```bash
pip install DocumentAI-std
```

## Quick Start

Here's a basic usage example demonstrating how to use the `Wildreceipt` dataset with **DocumentAI-std**.

### Example: Loading and Using the Wildreceipt Dataset

```python
from DocumentAI_std.datasets import Wildreceipt

# Load the training dataset
train_set = Wildreceipt(
    train=True,
    img_folder="/path/to/train/images/",
    label_path="/path/to/train/annotations.json",
)

# Load the test dataset
test_set = Wildreceipt(
    train=False,
    img_folder="/path/to/test/images/",
    label_path="/path/to/test/annotations.json",
)

# Assert the number of data samples in the train and test sets
assert len(train_set.data) == 1267
assert len(test_set.data) == 472
```

### Explanation:
- The `Wildreceipt` dataset is loaded by specifying the image folder and annotations path for both training and test data.
- `train=True` loads the training subset, while `train=False` loads the test subset.
- The number of data samples can be checked using the `data` attribute.

## Core Components

## VRDOM (Visually Rich Document Object Model)

**VRDOM** is a core component of `DocumentAI-std` that provides an abstraction layer for representing and manipulating document elements based on their visual structure. It allows users to analyze and extract meaningful information from documents, particularly those with complex layouts like invoices, receipts, and forms.

### Document Class

The `Document` class represents a visually rich document, consisting of content elements defined by bounding boxes, content type, and associated metadata.

#### Attributes:
- **img_path** (str): Path to the document image file.
- **ocr_output** (dict): OCR output with bounding boxes and content.
  - **bbox**: List of bounding box coordinates.
  - **content**: List of content strings corresponding to the bounding boxes.
- **elements** (List[DocElement]): A list of document elements (`DocElement` objects) representing individual content pieces.
- **device** (str): The device to be used for processing (default: "cpu").
  
#### Example Usage:

```python
from DocumentAI_std.base.document import Document

# Define OCR output for the document
ocr_output = {
    "bbox": [[10, 20, 100, 200], [110, 120, 180, 220]],
    "content": ["Total: $5.00", "Item: Coffee"]
}

# Create a Document instance
doc = Document(img_path="/path/to/document.jpg", ocr_output=ocr_output)

# Access the document's properties
print(f"Document filename: {doc.filename}")
print(f"Document shape: {doc.shape}")
print(f"Number of elements: {len(doc.elements)}")

# Serialize the document into JSON
doc_json = doc.to_json()
print(doc_json)
```

### DocElement Class

Each `Document` is composed of several `DocElement` objects. These represent individual content elements within the document (e.g., text boxes, images) and are typically defined by their bounding box and content.

#### Attributes:
- **x, y** (int): Coordinates for the bounding box's top-left corner.
- **w, h** (int): Width and height of the bounding box.
- **content_type** (ContentType): The type of content (e.g., text, image).
- **content** (Any): The content inside the bounding box.
- **device** (str): The processing device (e.g., "cpu").

#### Methods:
- **serialize**: Serializes the `DocElement` into a dictionary format for JSON compatibility.
- **area**: Calculates the area of the bounding box.
- **extract_pixels**: Extracts pixel data from the bounding box region of the image.

#### Example Usage:

```python
from DocumentAI_std.base.doc_element import DocElement, ContentType

# Create a document element
element = DocElement(x=10, y=20, w=100, h=50, content_type=ContentType.TEXT, content="Total: $5.00")

# Access properties
print(f"Bounding box: {element.x}, {element.y}, {element.w}, {element.h}")
print(f"Content: {element.content}")
print(f"Area: {element.area()}")

# Serialize the element
element_json = element.to_json()
print(element_json)
```

## Dataset Support

#### `Wildreceipt` Dataset
Represents the WildReceipt dataset for key information extraction, as introduced in ["Spatial Dual-Modality Graph Reasoning for Key Information Extraction"](https://arxiv.org/abs/2103.14470v1).

**Attributes:**
- `data`: List of document entities, including OCR and bounding box information.
- `root`: The root directory where document images are stored.
- `train`: Boolean indicating if the dataset is for training or testing.

#### `XFUND` Dataset
The XFUND dataset supports multilingual form understanding tasks. It’s designed for extracting structured information from documents in multiple languages.

#### `FUNSD` Dataset
The FUNSD dataset is focused on form understanding, useful for tasks that require extracting text and structured data from scanned forms.

#### `CORD` Dataset
The CORD dataset is designed for post-OCR parsing of consolidated receipt documents.

---

## Additional Features

- **OCR Integration**: The `Document` class can seamlessly ingest OCR outputs, structuring the raw text into a well-organized document representation. This is particularly useful for downstream tasks such as information extraction, table parsing, and content classification. For example, you can input OCR data from an invoice and easily extract line items, total amounts, or vendor details for further processing.

  ```python
  ocr_output = [{"text": "Invoice", "bbox": [10, 20, 200, 40]}, {"text": "Total: $500", "bbox": [10, 50, 200, 70]}]
  document = Document.from_ocr(ocr_output)
  ```

- **Serialization**: The `Document` and `DocElement` classes provide methods to serialize their structures into JSON-compatible dictionaries. This enables you to export or save documents for further analysis in a structured format.

  ```python
  serialized_doc = document.to_dict()
  # Output JSON representation of the document
  ```

- **Distance Calculations**: The library includes multiple utilities for calculating distances between elements within a document, which is useful for layout analysis and spatial relationships.

  - **Euclidean Distance**: Measures the straight-line distance between two points.
  - **Manhattan Distance**: Computes the distance along grid-like paths (right angles).
  - **Chebyshev Distance**: Identifies the maximum distance across any axis between two points.

  These can be leveraged for tasks like determining the proximity of elements in forms or detecting alignment in scanned documents.

  ```python
  dist = Distance.euclidean((x1, y1), (x2, y2))
  ```

- **Image Utilities**: The `ImageUtils` class provides essential functions for image analysis, including:
  - **Entropy Calculation**: Measures the randomness of pixel values, which is useful for detecting areas with high detail.
  - **Gabor Filters**: Generates Gabor filters for advanced texture analysis, often used in image segmentation.

  For instance, to calculate entropy within a document image:

  ```python
  entropy = ImageUtils.calculate_entropy(image, bbox)
  ```

- **Textual Utilities**: The library includes tools to handle various text-processing tasks, such as:
  - **Levenshtein Distance**: Measures how different two strings are, useful for fuzzy matching.
  - **Special Character Identification**: Detects symbols or special characters in text.
  - **Numeric Percentage Calculation**: Computes the percentage of numeric characters in a text, useful for extracting financial data.
  - **Date Detection**: Recognizes whether a string contains a date, useful in form and document parsing.

  ```python
  is_date = TextUtils.is_date("2024-09-13")
  ```

- **Layout Utilities**: Analyze the spatial layout of document elements with built-in functions:
  - **Horizontal and Vertical Alignment**: Determines if elements are aligned in a row or column.
  - **Overlap Calculation**: Calculates how much two bounding boxes overlap, which can help identify related fields in forms.
  - **Relative Positioning**: Checks whether an element is positioned in the top, middle, or bottom portion of a document.

  ```python
  is_aligned = LayoutUtils.is_horizontally_aligned(element1, element2)
  ```

- **OCR Adapter**: The `OCRAdapter` class simplifies the integration of various OCR engines, including PaddleOCR, EasyOCR, and Tesseract. It standardizes OCR outputs, making it easy to pass OCR results into the `Document` class regardless of the engine used. This ensures a consistent workflow for analyzing OCR results across different engines.

  ```python
  ocr_adapter = OCRAdapter(engine="Tesseract")
  ocr_output = ocr_adapter.run_ocr(image)
  document = Document.from_ocr(ocr_output)
  ```

---

## Contributing

Contributions to **DocumentAI-std** are welcome! If you’d like to contribute, please follow these steps:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

Make sure to follow the [contribution guidelines](https://github.com/LATIS-DocumentAI-Group/DocumentAI-std/blob/main/CONTRIBUTING.md) for more details.

## License

**DocumentAI-std** is licensed under the MIT License. See the [LICENSE](https://github.com/LATIS-DocumentAI-Group/DocumentAI-std/blob/master/LICENSE) file for more details.

