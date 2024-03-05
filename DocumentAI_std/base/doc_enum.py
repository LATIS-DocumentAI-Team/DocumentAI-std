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


class ContentRelativePosition(Enum):
    """
    Enum representing the relative position of a bounding box in a document.

    Attributes:
        TOP_HEIGHT (int): Bounding box exists at the top of the document.
        CENTRAL_HEIGHT (int): Bounding box exists in the central part of the document.
        BOTTOM_HEIGHT (int): Bounding box exists at the bottom of the document.

    Description:
    The position of a bounding box (BBT) in the document is categorized into three horizontal parts:
    - TOP_HEIGHT: At the top of the document.
    - CENTRAL_HEIGHT: In the middle of the document.
    - BOTTOM_HEIGHT: At the bottom of the document.

    The table below describes the variable 'Position':

    | Position         | Description                                  |
    |------------------|----------------------------------------------|
    | TOP_HEIGHT       | BBT exists at the top of the document.       |
    | CENTRAL_HEIGHT   | BBT exists in the central part of the document. |
    | BOTTOM_HEIGHT    | BBT exists at the bottom of the document.    |
    """

    TOP_HEIGHT = 1
    CENTRAL_HEIGHT = 2
    BOTTOM_HEIGHT = 3


class HorizontalAlignment(Enum):
    """
    Enum representing the relative position of a bounding box in a document.

    Attributes:
        TOP_HEIGHT (int): Bounding box exists at the top of the document.
        CENTRAL_HEIGHT (int): Bounding box exists in the central part of the document.
        BOTTOM_HEIGHT (int): Bounding box exists at the bottom of the document.

    Description:
    The position of a bounding box (BBT) in the document is categorized into three horizontal parts:
    - TOP_HEIGHT: At the top of the document.
    - CENTRAL_HEIGHT: In the middle of the document.
    - BOTTOM_HEIGHT: At the bottom of the document.

    The table below describes the variable 'Position':

    | Position         | Description                                  |
    |------------------|----------------------------------------------|
    | TOP_HEIGHT       | BBT exists at the top of the document.       |
    | CENTRAL_HEIGHT   | BBT exists in the central part of the document. |
    | BOTTOM_HEIGHT    | BBT exists at the bottom of the document.    |
    """

    RIGHT = 1
    CENTER = 2
    LEFT = 3


class VerticalAlignment(Enum):
    """
    Enum representing the relative position of a bounding box in a document.

    Attributes:
        TOP_HEIGHT (int): Bounding box exists at the top of the document.
        CENTRAL_HEIGHT (int): Bounding box exists in the central part of the document.
        BOTTOM_HEIGHT (int): Bounding box exists at the bottom of the document.

    Description:
    The position of a bounding box (BBT) in the document is categorized into three horizontal parts:
    - TOP_HEIGHT: At the top of the document.
    - CENTRAL_HEIGHT: In the middle of the document.
    - BOTTOM_HEIGHT: At the bottom of the document.

    The table below describes the variable 'Position':

    | Position         | Description                                  |
    |------------------|----------------------------------------------|
    | TOP_HEIGHT       | BBT exists at the top of the document.       |
    | CENTRAL_HEIGHT   | BBT exists in the central part of the document. |
    | BOTTOM_HEIGHT    | BBT exists at the bottom of the document.    |
    """

    TOP = 1
    MIDDLE = 2
    BOTTOM = 3
