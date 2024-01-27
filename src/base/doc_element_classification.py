from src.base.content_type import ContentType
from src.base.doc_element import DocElement


class DocElementClassification(DocElement):
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        content_type: ContentType,
        content,
        label: int,
    ):
        super().__init__(x, y, w, h, content_type, content)
        self.__label = label

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        self.__label = value

    def to_json(self):
        doc_element_dict = super().to_json()
        doc_element_dict["label"] = self.__label
        return doc_element_dict
