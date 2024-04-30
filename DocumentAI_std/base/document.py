import os
from typing import Any, List

from PIL import Image

from DocumentAI_std.base.doc_element import DocElement
from DocumentAI_std.base.doc_enum import ContentType


class Document:
    """
    Represents a document consisting of content elements defined by bounding boxes.

    A document is characterized by its content, where each content element is represented by a bounding box
    with associated content and content type.

    The `elements` attribute contains all the document elements, structured as follows:
    self.elements: List[DocElement]
    The `filename` attribute contains the filename of the document:
    self.filename: str
    The `shape` attribute contains the shape of the document:
    self.shape: tuple[int, int]

    Attributes:
        img_path (str): The path to the document image file.
        ocr_output (dict): The output of an OCR engine, containing bounding box and content information.
            Format: {
                bbox: List[List]
                content: List[Any]
            }
        device (str): The device to use for processing (default is "cpu").

    Example:
    >>> ocr_output = {
    ...     "bbox": [[10, 20, 30, 40], [50, 60, 70, 80]],
    ...     "content": ["Text 1", "Text 2"]
    ... }
    >>> doc = Document(img_path="/path/to/document.jpg", ocr_output=ocr_output)
    """

    def __init__(
        self, img_path: str, ocr_output: dict, device="cpu", **kwargs: Any
    ) -> None:
        """
        Initialize a Document instance with the provided image path and OCR output.

        Args:
            img_path (str): The path to the document image file.
            ocr_output (dict): The output of an OCR engine, containing bounding box and content information.
            device (str): The device to use for processing (default is "cpu").
            **kwargs: Additional keyword arguments.

        Raises:
            FileNotFoundError: If the specified image file path does not exist.
            AssertionError: If the lengths of bounding box and content lists in the OCR output do not match.
        """
        # File existence check
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"unable to locate img_folder at {img_path}")

        # Get the image shape
        self.__shape = Image.open(img_path).size
        self.__filename = os.path.basename(img_path)
        self.__img_path = img_path
        self.device = device
        try:
            assert len(ocr_output["bbox"]) == len(ocr_output["content"])
        except AssertionError:
            raise AssertionError(
                "Length of 'bbox' and 'content' in OCR output are not equal."
            )
        self.__elements: List[DocElement] = [
            DocElement(
                *bbox,
                content_type=ContentType.TEXT,
                content=content,
                img_path=self.__img_path,
                device=self.device,
            )
            for bbox, content in zip(ocr_output["bbox"], ocr_output["content"])
        ]

    @property
    def shape(self) -> tuple[int, int]:
        """Getter method for the shape attribute."""
        return self.__shape

    @shape.setter
    def shape(self, value: tuple[int, int]) -> None:
        """Setter method for the shape attribute."""
        self.__shape = value

    @property
    def img_path(self) -> str:
        """Getter method for the img_path attribute."""
        return self.__img_path

    @img_path.setter
    def img_path(self, value: str) -> None:
        """Setter method for the img_path attribute."""
        self.__img_path = value

    @property
    def filename(self) -> str:
        """Getter method for the filename attribute."""
        return self.__filename

    @filename.setter
    def filename(self, value: str) -> None:
        """Setter method for the filename attribute."""
        self.__filename = value

    @property
    def elements(self) -> List[List[DocElement]]:
        """Getter method for the elements attribute."""
        return self.__elements

    @elements.setter
    def elements(self, value: List[List[DocElement]]) -> None:
        """Setter method for the elements attribute."""
        self.__elements = value

    def serialize(self):
        """
        Serialize the Document object attributes into a JSON representing its state.

        Returns:
            dict: A dictionary containing the serialized representation of the Document object.
                  The dictionary includes the following keys:
                  - "filename": The filename of the document.
                  - "elements": A list of serialized representations of each document element.
                                Each element is represented as a dictionary.
                                For each element, the dictionary includes the serialized attributes
                                returned by the `serialize` method of the DocElement class.
        """
        return {
            "filename": self.__filename,
            "elements": [element.serialize() for element in self.__elements],
        }

    def to_json(self) -> dict:
        """
        Convert the document elements to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary representing the document elements with filename, bounding box,
                  content type, and content lists.
        """
        return {
            "filename": self.__filename,
            "bbox_list": [
                doc_element.to_json()["bbox"] for doc_element in self.__elements
            ],
            "content_type_list": [
                doc_element.to_json()["content_type"] for doc_element in self.__elements
            ],
            "content_list": [
                doc_element.to_json()["content"] for doc_element in self.__elements
            ],
        }
