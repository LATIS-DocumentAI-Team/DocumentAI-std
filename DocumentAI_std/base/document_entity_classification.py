from typing import Any

from DocumentAI_std.base.doc_enum import ContentType

from DocumentAI_std.base.doc_element_classification import DocElementClassification

from DocumentAI_std.base.document import Document


class DocumentEntityClassification(Document):
    """
    Represents a document consisting of content elements defined by bounding boxes.

    The class describes a document by its content, where each document element is defined by:
        - file_name: str
        - bounding boxes: List[List]
        - content: content of each bounding box: List
        - content_type: type of each bounding box content: Enum.ContentType
        - Label: The label or the class of each bounding box (Labels are not one-hot encoded)

    The `elements` attribute contains all the document elements within the filename, structured as follows:
    self.elements: List[str, List[DocumentEntityClassification]]

    Attributes:
        img_path (str): The path to the document image file.
        ocr_output (dict): The output of an OCR engine, containing bounding box, content, and label information.
            Format:
            {
                bbox: List[List]
                content: List[Any]
                label: List[Any]
            }
        root (str): The root directory of the document image file.

    Example:
    >>> ocr_output = {
    ...     "bbox": [[10, 20, 30, 40], [50, 60, 70, 80]],
    ...     "content": ["Text 1", "Text 2"],
    ...     "label": [0, 1]
    ... }
    >>> doc = DocumentEntityClassification(img_path="/path/to/document.jpg", ocr_output=ocr_output)
    """

    def __init__(self, img_path: str, ocr_output: dict, **kwargs: Any) -> None:
        super().__init__(img_path, ocr_output, **kwargs)
        self.elements = [
            DocElementClassification(
                *bbox,
                content_type=ContentType.TEXT,
                content=content,
                label=label,
                img_path=img_path
            )
            for bbox, content, label in zip(
                ocr_output["bbox"], ocr_output["content"], ocr_output["label"]
            )
        ]

    def to_json(self):
        return {
            "filename": self.filename,
            "bbox_list": [
                doc_element.to_json()["bbox"] for doc_element in self.elements
            ],
            "content_type_list": [
                doc_element.to_json()["content_type"] for doc_element in self.elements
            ],
            "content_list": [
                doc_element.to_json()["content"] for doc_element in self.elements
            ],
            "label": [doc_element.to_json()["label"] for doc_element in self.elements],
        }
