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
    Enum representing the horizontal alignment of a bounding box relative to another bounding box.

    Attributes:
        RIGHT (int): Bounding box exists at the right of another bounding box.
        CENTER (int): Bounding box exists in the central part of another bounding box.
        LEFT (int): Bounding box exists at the left of another bounding box.

    Description:
    The position of a bounding box (BBT) in the document is categorized into three horizontal parts:
    - RIGHT: At the right of another bounding box.
    - CENTER: In the central part of another bounding box.
    - LEFT: At the left of another bounding box.

    The table below describes the variable 'Position':

    | Position | Description                                |
    |----------|--------------------------------------------|
    | RIGHT    | BBT exists at the right of another bounding box. |
    | CENTER   | BBT exists in the central part of another bounding box. |
    | LEFT     | BBT exists at the left of another bounding box. |

    """

    RIGHT = 1
    CENTER = 2
    LEFT = 3


class VerticalAlignment(Enum):
    """
    Enum representing the vertical alignment of a bounding box relative to another bounding box.

    Attributes:
        TOP (int): Bounding box exists at the top of another bounding box.
        MIDDLE (int): Bounding box exists in the middle part of another bounding box.
        BOTTOM (int): Bounding box exists at the bottom of another bounding box.

    Description:
    The position of a bounding box (BBT) in the document is categorized into three vertical parts:
    - TOP: At the top of another bounding box.
    - MIDDLE: In the middle part of another bounding box.
    - BOTTOM: At the bottom of another bounding box.

    The table below describes the variable 'Position':

    | Position | Description                                |
    |----------|--------------------------------------------|
    | TOP      | BBT exists at the top of another bounding box. |
    | MIDDLE   | BBT exists in the middle part of another bounding box. |
    | BOTTOM   | BBT exists at the bottom of another bounding box. |

    """

    TOP = 1
    MIDDLE = 2
    BOTTOM = 3
