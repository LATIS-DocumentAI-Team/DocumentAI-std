# Documentation for `base`

## Package Documentation

## File: `doc_enum.py`

### Overview:
This module contains several `Enum` classes representing various positional and content types in document analysis. These enums are used to standardize the representation of the spatial and content characteristics of document elements such as bounding boxes.

---

### Class: `ContentRelativePosition`
An enumeration representing the relative vertical position of a bounding box (BBT) in a document. It categorizes a bounding box into three horizontal zones: top, central, and bottom.

#### Attributes:
- **`TOP_HEIGHT (int)`**: The bounding box is located in the top section of the document.
- **`CENTRAL_HEIGHT (int)`**: The bounding box is located in the central section of the document.
- **`BOTTOM_HEIGHT (int)`**: The bounding box is located in the bottom section of the document.

#### Description:
This enum divides the document into three primary vertical regions:
- `TOP_HEIGHT`: The bounding box is positioned in the upper part of the document.
- `CENTRAL_HEIGHT`: The bounding box is positioned in the middle part of the document.
- `BOTTOM_HEIGHT`: The bounding box is positioned in the lower part of the document.

#### Positional Breakdown:
The table below provides a summary of each position category:

| Position       | Description                                      |
|----------------|--------------------------------------------------|
| `TOP_HEIGHT`   | Bounding box is at the top section of the document. |
| `CENTRAL_HEIGHT` | Bounding box is in the central section of the document. |
| `BOTTOM_HEIGHT` | Bounding box is at the bottom section of the document. |

---

### Class: `ContentType`
An enumeration representing different types of content that can be contained within a document element.

#### Attributes:
- **`TEXT`**: Represents text content.
- **`IMAGE`**: Represents image content.
- **`GRAPHIC`**: Represents graphic content, such as drawings or shapes.
- **`TABLE`**: Represents tabular content, such as grids or tables.

#### Example:
```python
class ContentType(Enum):
    TEXT = 1
    IMAGE = 2
    GRAPHIC = 3
    TABLE = 4
```

---

### Class: `Enum`
A base class for creating enumerations, which are collections of name/value pairs.

#### Example:
```python
class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
```

#### Usage:
- **Attribute Access**: Access an enum member using its name.
  ```python
  Color.RED  # Output: <Color.RED: 1>
  ```
  
- **Value Lookup**: Retrieve an enum member using its value.
  ```python
  Color(1)  # Output: <Color.RED: 1>
  ```

- **Name Lookup**: Retrieve an enum member using its name as a string.
  ```python
  Color['RED']  # Output: <Color.RED: 1>
  ```

#### Additional Features:
- Enumerations support iteration:
  ```python
  list(Color)  # Output: [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
  ```

- Enumerations can have custom methods and member attributes.

---

### Class: `HorizontalAlignment`
An enumeration representing the horizontal alignment of a bounding box relative to another bounding box.

#### Attributes:
- **`RIGHT (int)`**: The bounding box is aligned to the right of another bounding box.
- **`CENTER (int)`**: The bounding box is aligned centrally with another bounding box.
- **`LEFT (int)`**: The bounding box is aligned to the left of another bounding box.

#### Description:
This enum categorizes the horizontal alignment of a bounding box into three parts:
- `RIGHT`: Positioned to the right of another bounding box.
- `CENTER`: Positioned centrally with respect to another bounding box.
- `LEFT`: Positioned to the left of another bounding box.

#### Positional Breakdown:

| Position | Description                                      |
|----------|--------------------------------------------------|
| `RIGHT`  | Bounding box is aligned to the right of another bounding box. |
| `CENTER` | Bounding box is aligned centrally with another bounding box. |
| `LEFT`   | Bounding box is aligned to the left of another bounding box. |

---

### Class: `VerticalAlignment`
An enumeration representing the vertical alignment of a bounding box relative to another bounding box.

#### Attributes:
- **`TOP (int)`**: The bounding box is aligned to the top of another bounding box.
- **`MIDDLE (int)`**: The bounding box is aligned to the middle part of another bounding box.
- **`BOTTOM (int)`**: The bounding box is aligned to the bottom of another bounding box.

#### Description:
This enum categorizes the vertical alignment of a bounding box into three parts:
- `TOP`: Positioned above another bounding box.
- `MIDDLE`: Positioned in the middle with respect to another bounding box.
- `BOTTOM`: Positioned below another bounding box.

#### Positional Breakdown:

| Position | Description                                      |
|----------|--------------------------------------------------|
| `TOP`    | Bounding box is aligned above another bounding box. |
| `MIDDLE` | Bounding box is aligned centrally (vertically) with another bounding box. |
| `BOTTOM` | Bounding box is aligned below another bounding box. |

---

This enhanced version improves the documentation by providing clearer descriptions, code examples where applicable, and better formatting for readability.

## File: document.py

### Class `Document`

Represents a document consisting of content elements defined by bounding boxes.

A `Document` object is characterized by its elements, each represented by a bounding box with associated content and type. These elements are stored in:
- `self.elements`: A list of `DocElement` objects.
- `self.filename`: The filename of the document.
- `self.shape`: The dimensions of the document, stored as a tuple `(width, height)`.

Attributes:
- `img_path` (str): Path to the document's image file.
- `ocr_output` (dict): OCR output containing bounding boxes and content information in the format:
  ```python
  {
      'bbox': List[List[int]],
      'content': List[Any]
  }
  ```
- `device` (str): Specifies the processing device (default is `"cpu"`).

Example usage:
```python
ocr_output = {
    'bbox': [[10, 20, 30, 40], [50, 60, 70, 80]],
    'content': ["Text 1", "Text 2"]
}
doc = Document(img_path="/path/to/document.jpg", ocr_output=ocr_output)
```

#### Method `__init__`

Initializes the `Document` instance with an image path and OCR output.

Args:
- `img_path` (str): Path to the document's image file.
- `ocr_output` (dict): Output from the OCR engine.
- `device` (str): Specifies the processing device (default is `"cpu"`).
- `**kwargs`: Additional keyword arguments.

Raises:
- `FileNotFoundError`: If the image file path is invalid.
- `AssertionError`: If the bounding boxes and content lists have mismatched lengths.

#### Method `serialize`

Serializes the `Document` object to a dictionary format.

Returns:
- `dict`: Serialized representation of the document, containing:
  - `"filename"`: The document's filename.
  - `"elements"`: A list of serialized elements from the document.

#### Method `to_json`

Converts the document elements to a JSON-compatible dictionary.

Returns:
- `dict`: A dictionary containing the document's filename, bounding boxes, content type, and content.

---

## File: document_entity_classification.py

### Class `DocumentEntityClassification`

Represents a document where content elements are defined by bounding boxes and categorized by a label.

The class stores document elements, each characterized by:
- `file_name`: The name of the file.
- `bounding boxes`: Coordinates of each bounding box.
- `content`: Text or content inside the bounding boxes.
- `content_type`: Type of content (using `Enum.ContentType`).
- `label`: Classification label for each bounding box.

Attributes:
- `img_path` (str): Path to the document image file.
- `ocr_output` (dict): Output from OCR containing bounding boxes, content, and labels in the format:
  ```python
  {
      'bbox': List[List[int]],
      'content': List[Any],
      'label': List[Any]
  }
  ```
- `root` (str): The root directory of the document image.

Example usage:
```python
ocr_output = {
    'bbox': [[10, 20, 30, 40], [50, 60, 70, 80]],
    'content': ["Text 1", "Text 2"],
    'label': [0, 1]
}
doc = DocumentEntityClassification(img_path="/path/to/document.jpg", ocr_output=ocr_output)
```

#### Method `__init__`

Initializes the `DocumentEntityClassification` instance with an image path and OCR output.

Args:
- `img_path` (str): Path to the document image file.
- `ocr_output` (dict): OCR output containing bounding boxes and content.
- `device` (str): Specifies the processing device (default is `"cpu"`).
- `**kwargs`: Additional keyword arguments.

Raises:
- `FileNotFoundError`: If the image file path is invalid.
- `AssertionError`: If the bounding boxes and content lists have mismatched lengths.

#### Method `serialize`

Serializes the `DocumentEntityClassification` object.

Returns:
- `dict`: Serialized dictionary representation of the document object containing:
  - `"filename"`: The document's filename.
  - `"elements"`: A list of serialized document elements.

#### Method `to_json`

Converts the document elements into a JSON-compatible format.

Returns:
- `dict`: JSON representation of document elements, with filename, bounding boxes, content type, and content.

---

## File: doc_element_classification.py

### Class `DocElementClassification`

Represents an individual content element in a document, usually defined by a bounding box.

Attributes:
- `x` (int): X-coordinate of the bounding box.
- `y` (int): Y-coordinate of the bounding box.
- `w` (int): Width of the bounding box.
- `h` (int): Height of the bounding box.
- `content_type` (`ContentType`): Type of the content within the bounding box.
- `content` (Any): The content inside the bounding box.
- `device` (str): Device for processing (default is `"cpu"`).

Example usage:
```python
doc_element = DocElementClassification(x=10, y=20, w=100, h=50, content_type=ContentType.TEXT, content="Hello, world!")
```

#### Method `__init__`

Initializes a `DocElementClassification` instance.

#### Method `area`

Calculates the area of the bounding box.

Returns:
- `float`: Area calculated as `width * height`.

#### Method `extract_pixels`

Extracts pixel values from the bounding box region.

Args:
- `is_gray` (bool): Whether to convert the region to grayscale. Defaults to `True`.

Returns:
- `torch.Tensor`: A tensor of pixel values.

#### Method `serialize`

Serializes the `DocElementClassification` object.

Returns:
- `dict`: Serialized representation of the element containing:
  - Coordinates (`x`, `y`), dimensions (`w`, `h`), content type, content, label, and image path.

#### Method `to_json`

Converts the element to a JSON-compatible dictionary.

Returns:
- `dict`: JSON representation of the document element.

---

## File: doc_element.py

### Class `DocElement`

Represents an individual content element within a document.

Attributes:
- `x` (int): X-coordinate of the bounding box.
- `y` (int): Y-coordinate of the bounding box.
- `w` (int): Width of the bounding box.
- `h` (int): Height of the bounding box.
- `content_type` (`ContentType`): Type of the content within the bounding box.
- `content` (Any): The content inside the bounding box.
- `device` (str): Device for processing (default is `"cpu"`).

Example usage:
```python
doc_element = DocElement(x=10, y=20, w=100, h=50, content_type=ContentType.TEXT, content="Hello, world!")
```

#### Method `__init__`

Initializes a `DocElement` instance.

#### Method `area`

Calculates the bounding box's area.

Returns:
- `float`: Area calculated as `width * height`.

#### Method `extract_pixels`

Extracts the pixels from the bounding box region.

Args:
- `is_gray` (bool): Whether to convert the extracted region to grayscale. Defaults to `True`.

Returns:
- `torch.Tensor`: A tensor representing the pixel values in the bounding box.

#### Method `serialize`

Serializes the `DocElement` object.

Returns:
- `dict`: Serialized dictionary containing:
  - Coordinates (`x`, `y`), dimensions (`w`, `h`), content type, and content.

#### Method `to_json`

Converts the element into a JSON-compatible dictionary.

Returns:
- `dict`: JSON representation of the document element.


# Documentation for `utils`

## Package Documentation

## File: `image_utils.py`

### Class `ImageUtils`

#### Method `entropy`

Compute the entropy of a document element's pixel values.

This method calculates the entropy of the pixel values within the bounding box of the specified document element.

**Args:**
- `doc_element` (DocElement): The document element containing pixel values.

**Returns:**
- `float`: The entropy value of the pixel values within the document element.

**Note:**
- Entropy is a measure of uncertainty or randomness in the pixel values of an image. Higher entropy indicates higher disorder or unpredictability in the pixel values.

**Raises:**
- `ValueError`: If the document element does not contain valid pixel values.

#### Method `gabor_blank_filter`

Generates a custom Gabor filter.

**Args:**
- `doc_element` (DocElement): The document element containing pixel values.
- `scales` (int): Number of scales (frequencies).
- `orientations` (int): Number of orientations.

**Returns:**
- `torch.Tensor`: A tensor with shape `(scales, orientations, doc_element.h, doc_element.w)`.

#### Method `gabor_decomposition`

Obtains the Gabor feature vector of an input image.

**Args:**
- `doc_element` (DocElement): The document element containing pixel values.
- `scales` (int): Number of scales (frequencies).
- `orientations` (int): Number of orientations.
- `d1` (int): The factor of downsampling along rows.
- `d2` (int): The factor of downsampling along columns.

**Returns:**
- `torch.Tensor`: A tensor with shape `(doc_element.h // d1, doc_element.w // d2, (scales * orientations) / (d1 * d2))`.

#### Method `gabor_feature`

Extracts the Gabor features of an input image.

**Args:**
- `doc_element` (DocElement): The document element containing pixel values.
- `scales` (int): Number of scales (frequencies).
- `orientations` (int): Number of orientations.
- `d1` (int): The factor of downsampling along rows.
- `d2` (int): The factor of downsampling along columns.

**Returns:**
- `torch.Tensor`: A tensor with shape `(doc_element.h // d1, doc_element.w // d2, (scales * orientations) / (d1 * d2))`.

---

## File: `base_utils.py`

### Class `BaseUtils`

#### Method `X1X2X3X4_to_xywh`

Converts bounding box coordinates from `(x1, y1, x2, y2, x3, y3, x4, y4)` format to `(x, y, w, h)` format.

#### Method `X1X2_to_xywh`

Converts bounding box coordinates from `(x1, y1, x2, y2)` format to `(x, y, w, h)` format.


## File: `text_utils.py`

### Method `calculate_numeric_percentage`

Calculates the percentage of numeric characters in the content of a `DocElement` of type `TEXT`.

**Args:**
- `doc_element (DocElement)`: The document element whose content's numeric character percentage is to be calculated.

**Returns:**
- `float`: The percentage of numeric characters in the content.

**Raises:**
- `AssertionError`: If the content type of the `DocElement` is not `TEXT`.

### Method `count_special_chars`

Counts the number of special characters in the content of a `DocElement` of type `TEXT`.

**Args:**
- `doc_element (DocElement)`: The document element from which to count special characters.

**Returns:**
- `int`: The number of special characters in the content.

**Raises:**
- `AssertionError`: If the content type of the `DocElement` is not `TEXT`.

### Method `has_special_char`

Checks if the content of a `DocElement` of type `TEXT` contains any special characters.

**Args:**
- `doc_element (DocElement)`: The document element to check for special characters.

**Returns:**
- `bool`: `True` if the content contains special characters; `False` otherwise.

**Raises:**
- `AssertionError`: If the content type of the `DocElement` is not `TEXT`.

### Method `is_date`

Determines if the given text contains a date in various formats.

**Args:**
- `doc_element (DocElement)`: The document element to check for a date.

**Returns:**
- `bool`: `True` if the text contains a date; `False` otherwise.

**Raises:**
- `AssertionError`: If the content type of the `DocElement` is not `TEXT`.

### Method `levenshtein_distance`

Computes the Levenshtein distance between the contents of two `DocElement` objects.

**Args:**
- `a (DocElement)`: The first document element.
- `b (DocElement)`: The second document element.

**Returns:**
- `int`: The Levenshtein distance between the contents of the two `DocElement` objects.

**Raises:**
- `AssertionError`: If either `DocElement` does not contain text content.

### Method `nbr_chars`

Counts the number of characters in the content of a `DocElement` if it is of type `TEXT`.

**Args:**
- `doc_element (DocElement)`: The document element from which to count characters.

**Returns:**
- `int`: The number of characters in the content.

**Raises:**
- `AssertionError`: If the content type of the `DocElement` is not `TEXT`.


## File: `OCR_adapter.py`

### Method `X1X2X3X4_to_xywh`

Converts bounding box coordinates from `(x1, y1, x2, y2, x3, y3, x4, y4)` format to `(x, y, w, h)` format.

### Method `X1X2_to_xywh`

Converts bounding box coordinates from `(x1, y1, x2, y2)` format to `(x, y, w, h)` format.

### Class `OCRAdapter`

An adapter class for standardizing OCR outputs from various engines.

This class provides a unified interface to convert OCR results obtained from different engines, such as PaddleOCR, EasyOCR, and Tesseract, into a consistent format for easier handling, processing, and analysis.

**Attributes:**
- `ocr_method (str)`: The OCR method currently in use for processing.
- `lang (List[str])`: The language(s) specified for OCR processing.

**Methods:**
- `__init__(ocr_method: str, lang: List[str])`: Initializes the `OCRAdapter` instance with the specified OCR method and language settings.
- `apply_ocr(source: Union[str, io.BytesIO]) -> Document`: Applies OCR to the given source using the specified OCR method.
- `apply_easyocr(source: Union[str, io.BytesIO]) -> dict`: Applies OCR using EasyOCR.
- `apply_paddleocr(source: Union[str, io.BytesIO]) -> dict`: Applies OCR using PaddleOCR.
- `apply_tesseract_ocr(source: Union[str, io.BytesIO]) -> dict`: Applies OCR using Tesseract.
- `from_easy_ocr(easy_ocr_output)`: Converts EasyOCR output to a standardized format.
- `from_paddle_ocr(paddle_ocr_output)`: Converts PaddleOCR output to a standardized format.
- `from_tesseract_ocr(tesseract_ocr_output)`: Converts Tesseract OCR output to a standardized format.

### Method `__init__`

Initializes the `OCRAdapter` instance with the specified OCR method and language settings.

**Args:**
- `ocr_method (str)`: The OCR method to be used. Supported methods include "easyocr", "paddle", and "tesseract".
- `lang (List[str])`: A list of language codes specifying the languages for OCR. Example: `["en", "fr"]` for English and French.

### Method `_open_image`

Opens and converts an image file to RGB format.

**Args:**
- `source (Union[str, io.BytesIO])`: The source of the image file.

**Returns:**
- `Image.Image`: The image object in RGB format.

### Method `apply_easy_ocr`

Applies OCR using EasyOCR.

**Args:**
- `source (Union[str, io.BytesIO])`: The source of the image file for OCR.

**Returns:**
- `dict`: The result of OCR.

### Method `apply_ocr`

Applies OCR to the given source using the specified OCR method.

**Args:**
- `source (Union[str, io.BytesIO])`: The source of the image file for OCR.

**Returns:**
- `Document`: A document object containing the source and OCR result.

**Raises:**
- `AssertionError`: If the specified OCR method is not recognized.

### Method `apply_paddleocr`

Applies OCR using PaddleOCR.

**Args:**
- `source (Union[str, io.BytesIO])`: The source of the image file for OCR.

**Returns:**
- `dict`: The result of OCR.

### Method `apply_tesseract_ocr`

Applies OCR using Tesseract.

**Args:**
- `source (Union[str, io.BytesIO])`: The source of the image file for OCR.

**Returns:**
- `dict`: The result of OCR.

### Method `from_easy_ocr`

Converts EasyOCR output to a standardized format.

**Args:**
- `easy_ocr_output (list)`: List containing OCR output from EasyOCR.

**Returns:**
- `dict`: Standardized OCR output with 'bbox' and 'content' keys.

### Method `from_paddle_ocr`

Converts PaddleOCR output to a standardized format.

**Args:**
- `paddle_ocr_output (list)`: List containing OCR output from PaddleOCR.

**Returns:**
- `dict`: Standardized OCR output with 'bbox' and 'content' keys.

### Method `from_tesseract_ocr`

Converts Tesseract OCR output to a standardized format.

**Args:**
- `tesseract_ocr_output (dict)`: Dictionary containing OCR output from Tesseract.

**Returns:**
- `dict`: Standardized OCR output with 'bbox' and 'content' keys.

### Method `__call__`

Calls the instance as a function.

### Method `ocr`

Performs OCR with PaddleOCR.

**Args:**
- `img`: The image for OCR, supporting `ndarray`, `img_path`, or `list` of `ndarray`.
- `det`: Whether to use text detection. If `False`, only text recognition is executed. Default is `True`.
- `rec`: Whether to use text recognition. If `False`, only text detection is executed. Default is `True`.
- `cls`: Whether to use angle classification. If `True`, text with 180-degree rotation can be recognized. Set to `False` for better performance if no 180-degree rotated text is expected. Text with 90 or 270-degree rotation can be recognized even with `cls=False`.
- `bin`: Whether to binarize the image to black and white. Default is `False`.
- `inv`: Whether to invert image colors. Default is `False`.
- `alpha_color`: RGB color tuple for transparent parts replacement. Default is pure white.


## File: `layout_utils.py`

### Method `angle_inter_element`

Calculates the angle between the centers of two `DocElement` bounding boxes.

**Args:**
- `a (DocElement)`: The first `DocElement`.
- `b (DocElement)`: The second `DocElement`.

**Returns:**
- `float`: The angle between the two `DocElement` centers, measured in radians.

**Note:**
- The angle is determined based on the centers of the bounding boxes of the `DocElement` objects.

### Method `calculate_horizontal_alignment`

Determines the horizontal alignment between two bounding boxes.

**Args:**
- `a (DocElement)`: The first bounding box.
- `b (DocElement)`: The second bounding box.

**Returns:**
- `HorizontalAlignment`: The horizontal alignment (`'left'`, `'center'`, or `'right'`).

### Method `calculate_overlap`

Computes the degree of overlap between two bounding boxes.

**Args:**
- `a (DocElement)`: The first bounding box.
- `b (DocElement)`: The second bounding box.

**Returns:**
- `float`: The degree of overlap between the bounding boxes.

### Method `calculate_vertical_alignment`

Determines the vertical alignment between two bounding boxes.

**Args:**
- `a (DocElement)`: The first bounding box.
- `b (DocElement)`: The second bounding box.

**Returns:**
- `VerticalAlignment`: The vertical alignment (`'top'`, `'middle'`, or `'bottom'`).

### Method `chebyshev_distance`

Calculates the Chebyshev distance between two points.

**Args:**
- `a (DocElement)`: The first point.
- `b (DocElement)`: The second point.

**Returns:**
- `float`: The Chebyshev distance between the two points.

### Method `euclidean_distance`

Computes the Euclidean distance between two points.

**Args:**
- `a (DocElement)`: The first point.
- `b (DocElement)`: The second point.

**Returns:**
- `float`: The Euclidean distance between the two points.

### Method `manhattan_distance`

Determines the Manhattan distance between two points.

**Args:**
- `a (DocElement)`: The first point.
- `b (DocElement)`: The second point.

**Returns:**
- `float`: The Manhattan distance between the two points.

### Method `relative_position`

Assesses the relative position of a bounding box within a document.

**Args:**
- `doc_element (DocElement)`: The bounding box element whose position is to be determined.
- `document (Document)`: The document containing the bounding box.

**Returns:**
- `ContentRelativePosition`: The relative position of the bounding box within the document.

**Note:**
- The document is divided into three vertical sections: top, center, and bottom. The vertical center of the bounding box is used to determine its position within these sections.


# Documentation for `datasets`

## Package Overview

## File: `wildreceipt.py`

### Method `X1X2X3X4_to_xywh`

Converts bounding box coordinates from the format `(x1, y1, x2, y2, x3, y3, x4, y4)` to `(x, y, w, h)`.

### Method `X1X2_to_xywh`

Converts bounding box coordinates from the format `(x1, y1, x2, y2)` to `(x, y, w, h)`.

### Class `Wildreceipt`

Represents the WildReceipt dataset, used in the paper ["Spatial Dual-Modality Graph Reasoning for Key Information Extraction"](https://arxiv.org/abs/2103.14470v1). The dataset can be downloaded from [this repository](https://download.openmmlab.com/mmocr/data/wildreceipt.tar).

**Args:**
- `img_folder (str)`: Directory containing all the dataset images.
- `label_path (str)`: Path to the dataset annotations file.
- `train (bool, optional)`: Indicates whether the subset is for training. Defaults to `True`.

**Attributes:**
- `data (List[DocumentEntityClassification])`: List of document entities in the dataset.
- `root (str)`: Root directory of the document image files.
- `train (bool)`: Indicates if the dataset is for training.

**Example:**
```python
>>> dataset = Wildreceipt(
...     img_folder="/path/to/images",
...     label_path="/path/to/annotations.json",
...     train=True
... )
```

### Method `__init__`

Initializes the `Wildreceipt` instance. Refer to `help(type(self))` for the precise signature.

## File: `xfund.py`

### Class `XFUND`

Represents the XFUND dataset, detailed in the paper ["XFUND"](https://openreview.net/pdf?id=SJl3z659UH).

**Args:**
- `img_folder (str)`: Directory containing all the dataset images.
- `label_path (str)`: Path to the dataset annotations file.
- `train (bool, optional)`: Indicates whether the subset is for training. Defaults to `True`.

**Attributes:**
- `data (List[DocumentEntityClassification])`: List of document entities in the dataset.
- `root (str)`: Root directory of the document image files.
- `train (bool)`: Indicates if the dataset is for training.

**Example:**
```python
>>> dataset = XFUND(
...     data_folder="/path/to/xfund/",
...     train=True
... )
```

### Method `__init__`

Initializes the `XFUND` instance. Refer to `help(type(self))` for the precise signature.

## File: `funsd.py`

### Class `FUNSD`

Represents the FUNSD dataset, used in the paper ["CORD: A Consolidated Receipt Dataset for Post-OCR Parsing"](https://openreview.net/pdf?id=SJl3z659UH).

**Args:**
- `img_folder (str)`: Directory containing all the dataset images.
- `label_path (str)`: Path to the dataset annotations file.
- `train (bool, optional)`: Indicates whether the subset is for training. Defaults to `True`.

**Attributes:**
- `data (List[DocumentEntityClassification])`: List of document entities in the dataset.
- `root (str)`: Root directory of the document image files.
- `train (bool)`: Indicates if the dataset is for training.

**Example:**
```python
>>> dataset = FUNSD(
...     data_folder="/path/to/funsd/",
...     train=True
... )
```

## File: `cord.py`

### Class `CORD`

Represents the CORD dataset, described in the paper ["CORD: A Consolidated Receipt Dataset for Post-OCR Parsing"](https://openreview.net/pdf?id=SJl3z659UH).

**Args:**
- `img_folder (str)`: Directory containing all the dataset images.
- `label_path (str)`: Path to the dataset annotations file.
- `train (bool, optional)`: Indicates whether the subset is for training. Defaults to `True`.

**Attributes:**
- `data (List[DocumentEntityClassification])`: List of document entities in the dataset.
- `root (str)`: Root directory of the document image files.
- `train (bool)`: Indicates if the dataset is for training.

**Example:**
```python
>>> dataset = CORD(
...     img_folder="/path/to/cord_train/image",
...     label_path="/path/to/cord_train/json",
...     train=True
... )
>>> dataset = CORD(
...     img_folder="/path/to/cord_test/image",
...     label_path="/path/to/cord_test/json",
...     train=False
... )
```

### Method `__init__`

Initializes the `CORD` instance. Refer to `help(type(self))` for the precise signature.

