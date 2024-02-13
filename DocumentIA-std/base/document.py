import os
from typing import Any, List, Tuple

from src.base.content_type import ContentType
from src.base.doc_element import DocElement


class Document:
    """
    The class describe a document by its content, a document in our case is defined by:
        file_name: str
        bounding boxes: List[List]
        content: content of each bounding box : List
        content_type: type of each bounding box content: Enum.ContentType

    :arg
        ---
        img_path: path to document
        ocr_output: define the output of an ocr, (here we assume it is a json format in the following format)
        {
            bbox: List[List]
            content: List[Any]
        }
        Here len(bbox) == len(content) an obligation

        bbox are in the format x,y,w,h
        this output are generate from an ocr engine
        ---
    """

    # TODO: add method to extract image when need depend on content
    def __init__(self, img_path: str, ocr_output: dict, **kwargs: Any) -> None:
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

    def to_json(self):
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
