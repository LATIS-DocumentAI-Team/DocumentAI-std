from typing import Any

from src.base.content_type import ContentType
from src.base.doc_element_classification import DocElementClassification
from src.base.document import Document


class DocumentEntityClassification(Document):
    """
    The class describe a document by its content, a document in our case is defined by:
        file_name: str
        bounding boxes: List[List]
        content: content of each bounding box : List
        content_type: type of each bounding box content: Enum.ContentType
        Label: The label or the class of each bounding box

    :arg
        ---
        img_path: path to document
        ocr_output: define the output of an ocr, (here we assume it is a json format in the following format)
        {
            bbox: List[List]
            content: List[Any]
            Label:  List[Any]
        }
        Here len(bbox) == len(content) == len(labels) an obligation

        bbox are in the format x,y,w,h
        (Labels are not one Hot encoded)
        this output are generate from an ocr engine
        ---
    """

    def __init__(self, img_path: str, ocr_output: dict, **kwargs: Any) -> None:
        super().__init__(img_path, ocr_output, **kwargs)
        self.elements[1] = [
            DocElementClassification(
                *bbox, content_type=ContentType.TEXT, content=content, label=label
            )
            for bbox, content, label in zip(
                ocr_output["bbox"], ocr_output["content"], ocr_output["label"]
            )
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
            "label": [
                doc_element.to_json()["label"] for doc_element in self.elements[1]
            ],
        }
