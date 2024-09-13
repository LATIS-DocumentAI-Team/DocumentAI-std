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