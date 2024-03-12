import torch
from PIL import Image
from torchvision import transforms

from DocumentAI_std.base.doc_enum import ContentType


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
        device (str): The device to use for processing (default is "cpu").

    Example:
    >>> doc_element = DocElement(x=10, y=20, w=100, h=50, content_type=ContentType.TEXT, content="Hello, world!")
    """

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        content_type: ContentType,
        content,
        img_path=None,
        device="cpu",
    ):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__content_type = content_type
        self.__content = content
        self.device = device
        self.img_path = img_path

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

    def serialize(self):
        """
        Serialize the DocElement object attributes into a JSON representing its state.

        Returns:
            dict: A dictionary containing the serialized representation of the object.
                  The dictionary includes the following keys:
                  - "x": The x-coordinate of the document element.
                  - "y": The y-coordinate of the document element.
                  - "w": The width of the document element.
                  - "h": The height of the document element.
                  - "content_type": The type of content contained in the document element.
                  - "content": The actual content of the document element.
        """
        return {
            "x": self.__x,
            "y": self.__y,
            "w": self.__w,
            "h": self.__h,
            "content_type": self.__content_type,
            "content": self.__content,
        }

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

    def area(self) -> float:
        """
        Calculate the area of a DocElement.

        Returns:
            float: The area of the DocElement, calculated as the product of its width (w) and height (h).
        """
        return self.__h * self.__w

    def extract_pixels(self, is_gray: bool = True) -> torch.Tensor:
        """
        Extract the pixels from the bounding box region of the image.

        Args:
            is_gray (bool, optional): Flag to convert the extracted region to grayscale. Defaults to True.

        Returns:
            torch.Tensor: A PyTorch tensor representing the pixels within the bounding box.
        """
        # Open the image using PIL
        image = Image.open(self.img_path)

        # Crop the image to extract the region of interest (ROI) using the bounding box coordinates
        roi = image.crop((self.__x, self.__y, self.__x + self.__w, self.__y + self.__h))

        # Convert the ROI to grayscale if necessary
        if is_gray and roi.mode != "L":
            roi = roi.convert("L")

        # Convert the PIL image to a PyTorch tensor
        transform = transforms.ToTensor()
        roi_tensor = transform(roi).to(self.device)

        return roi_tensor
