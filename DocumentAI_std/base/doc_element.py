from DocumentAI_std.base.content_type import ContentType


class DocElement:
    """
    Represents a basic element within a document, typically defined by bounding boxes.

    This class encapsulates properties and methods for managing document elements, including their
    position, size, content type, and content.

    Attributes:
        x (int): The x-coordinate of the document element (or bounding box).
        y (int): The y-coordinate of the document element (or bounding box).
        w (int): The width of the document element (or bounding box).
        h (int): The height of the document element (or bounding box).
        content_type (ContentType): The type of content contained in the document element.
        content (Any): The actual content of the document element.

    Example:
    >>> doc_element = DocElement(x=10, y=20, w=100, h=50, content_type=ContentType.TEXT, content="Hello, world!")
    """

    def __init__(
        self, x: int, y: int, w: int, h: int, content_type: ContentType, content
    ):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__content_type = content_type
        self.__content = content

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def w(self):
        return self.__w

    @w.setter
    def w(self, value):
        self.__w = value

    @property
    def h(self):
        return self.__h

    @h.setter
    def h(self, value):
        self.__h = value

    @property
    def content_type(self):
        return self.__content_type

    @content_type.setter
    def content_type(self, value):
        self.__content_type = value

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    def to_json(self):
        """
        Convert the document element to a JSON-compatible dictionary.

        :return: A dictionary representation of the document element.
        :rtype: dict
        """
        return {
            "bbox": [self.__x, self.__y, self.__w, self.__h],
            "content_type": self.__content_type,
            "content": self.__content,
        }
