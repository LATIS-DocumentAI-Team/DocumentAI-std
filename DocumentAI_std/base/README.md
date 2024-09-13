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

