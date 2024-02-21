import os
from typing import Any, List

from DocumentAI_std.base.content_type import ContentType

from DocumentAI_std.base.doc_element import DocElement


class Document:
    """
    Represents a document consisting of content elements defined by bounding boxes.

    A document is characterized by its content, where each content element is represented by a bounding box
    with associated content and content type.

    The `elements` attribute contains all the document elements, structured as follows:
    self.elements: List[str, List[DocElement]]

    Attributes:
        img_path (str): The path to the document image file.
        ocr_output (dict): The output of an OCR engine, containing bounding box and content information.
            Format: {
                bbox: List[List]
                content: List[Any]
            }
        root (str): The root directory of the document image file.

    Example:
    >>> ocr_output = {
    ...     "bbox": [[10, 20, 30, 40], [50, 60, 70, 80]],
    ...     "content": ["Text 1", "Text 2"]
    ... }
    >>> doc = Document(img_path="/path/to/document.jpg", ocr_output=ocr_output)
    """

    # TODO: add method to extract image when need depend on content
    def __init__(self, img_path: str, ocr_output: dict, **kwargs: Any) -> None:
        """
        Initialize a Document instance with the provided image path and OCR output.

        Args:
            img_path (str): The path to the document image file.
            ocr_output (dict): The output of an OCR engine, containing bounding box and content information.
            **kwargs: Additional keyword arguments.

        Raises:
            FileNotFoundError: If the specified image file path does not exist.
            AssertionError: If the lengths of bounding box and content lists in the OCR output do not match.
        """
        # File existence check
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"unable to locate img_folder at {img_path}")

        filename = os.path.basename(img_path)
        self.root = os.path.dirname(img_path)
        try:
            assert len(ocr_output["bbox"]) == len(ocr_output["content"])
        except AssertionError:
            raise AssertionError(
                "Length of 'bbox' and 'content' in OCR output are not equal."
            )

        self.elements: List[str, List[DocElement]] = [
            filename,
            [
                DocElement(*bbox, content_type=ContentType.TEXT, content=content)
                for bbox, content in zip(ocr_output["bbox"], ocr_output["content"])
            ],
        ]

    def to_json(self) -> dict:
        """
        Convert the document elements to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary representing the document elements with filename, bounding box,
                  content type, and content lists.
        """
        return {
            "filename": self.elements[0],
            "bbox_list": [
                doc_element.to_json()["bbox"] for doc_element in self.elements[1]
            ],
            "content_type_list": [
                doc_element.to_json()["content_type"]
                for doc_element in self.elements[1]
            ],
            "content_list": [
                doc_element.to_json()["content"] for doc_element in self.elements[1]
            ],
        }
