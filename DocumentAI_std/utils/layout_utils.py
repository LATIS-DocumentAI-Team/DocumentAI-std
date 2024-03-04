from typing import Tuple

from DocumentAI_std.base.document import Document

from DocumentAI_std.base.doc_element import DocElement
from DocumentAI_std.base.doc_enum import ContentRelativePosition


class LayoutUtils:
    @staticmethod
    def relative_position(
        doc_element: DocElement, document: Document
    ) -> ContentRelativePosition:
        """
        Determine the relative position of a bounding box within a document.

        Args:
            doc_element (DocElement): The bounding box element to determine the position for.
            document (Document): The document containing the bounding box.

        Returns:
            ContentRelativePosition: The relative position of the bounding box within the document.

        Note:
            The document's shape is divided into three vertical sections: top, center, and bottom.
            The bounding box's vertical center is used to determine its position within these sections.
        """
        # Extracting shape and bounding box information
        shape: Tuple[int, int] = document.shape
        bbox: Tuple[int, int, int, int] = (
            doc_element.x,
            doc_element.y,
            doc_element.w,
            doc_element.h,
        )

        # Calculate the vertical center of the bounding box
        bbox_center_y: float = bbox[1] + bbox[3] / 2

        # Calculate the boundaries of the document's top and bottom thirds
        top_third_boundary: float = shape[1] / 3
        bottom_third_boundary: float = shape[1] * 2 / 3

        # Check if the bbox center is in the top third, center third, or bottom third
        if bbox_center_y <= top_third_boundary:
            return ContentRelativePosition.TOP_HEIGHT
        elif top_third_boundary < bbox_center_y <= bottom_third_boundary:
            return ContentRelativePosition.CENTRAL_HEIGHT
        else:
            return ContentRelativePosition.BOTTOM_HEIGHT
