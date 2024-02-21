from enum import Enum


class ContentType(Enum):
    """
    Enumeration defining the types of content within a document element.

    Attributes:
        TEXT : Text content.
        IMAGE : Image content.
        GRAPHIC : Graphic content.
        TABLE : Tabular content.
    """

    TEXT = 1
    IMAGE = 2
    GRAPHIC = 3
    TABLE = 4
