from DocumentAI_std.base.doc_enum import ContentType

from DocumentAI_std.base.doc_element import DocElement


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
        img_path=None,
        device="cpu",
    ):
        super().__init__(x, y, w, h, content_type, content, img_path, device)
        self.__label = label

    """
    Represents a classified document element within a document, typically defined by bounding boxes.

    This class extends the functionality of the base `DocElement` class to include classification information,
    such as labels assigned to document elements.

    Attributes:
        x (int): The x-coordinate of the document element (or bounding box).
        y (int): The y-coordinate of the document element (or bounding box).
        w (int): The width of the document element (or bounding box).
        h (int): The height of the document element (or bounding box).
        content_type (ContentType): The type of content contained in the document element.
        content (Any): The actual content of the document element.
        label (int): The label assigned to the document element for classification purposes.

    Example:
    >>> doc_element = DocElementClassification(x=10, y=20, w=100, h=50, content_type=ContentType.TEXT, content="Hello, world!", label=1)
    """

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        self.__label = value

    def serialize(self):
        """
        Serialize the DocElementClassification object attributes into a JSON representing its state.

        Returns:
            dict: A dictionary containing the serialized representation of the object.
                  The dictionary includes the following keys:
                  - "x": The x-coordinate of the document element.
                  - "y": The y-coordinate of the document element.
                  - "w": The width of the document element.
                  - "h": The height of the document element.
                  - "content_type": The type of content contained in the document element.
                  - "content": The actual content of the document element.
                  - label (int): The label assigned to the document element for classification purposes.
                  - img_path: The image path assigned to the document element of the whole document.
                  - device: The device used.
        """
        return {
            "x": self.__x,
            "y": self.__y,
            "w": self.__w,
            "h": self.__h,
            "content_type": self.__content_type,
            "content": self.__content,
            "label": self.__label,
            "img_path": self.img_path,
            "device": self.device,
        }

    def to_json(self):
        """
        Convert the classified document element to a JSON-compatible dictionary.

        :return: A dictionary representation of the classified document element.
        :rtype: dict
        """
        doc_element_dict = super().to_json()
        doc_element_dict["label"] = self.__label
        return doc_element_dict
