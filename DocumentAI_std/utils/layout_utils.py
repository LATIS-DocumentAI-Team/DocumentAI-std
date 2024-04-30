import math
from typing import Tuple

from DocumentAI_std.base.document import Document

from DocumentAI_std.base.doc_element import DocElement
from DocumentAI_std.base.doc_enum import (
    ContentRelativePosition,
    HorizontalAlignment,
    VerticalAlignment,
)


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

    @staticmethod
    def euclidean_distance(a: DocElement, b: DocElement) -> float:
        """
        Compute the Euclidean distance between two points.

        Args:
            a (DocElement): The first point.
            b (DocElement): The second point.

        Returns:
            float: The Euclidean distance between the two points.
        """
        dx = a.x - b.x
        dy = a.y - b.y
        return math.sqrt(dx**2 + dy**2)

    @staticmethod
    def manhattan_distance(a: DocElement, b: DocElement) -> float:
        """
        Compute the Manhattan distance between two points.

        Args:
            a (DocElement): The first point.
            b (DocElement): The second point.

        Returns:
            float: The Manhattan distance between the two points.
        """
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        return dx + dy

    @staticmethod
    def chebyshev_distance(a: DocElement, b: DocElement) -> float:
        """
        Compute the Chebyshev distance between two points.

        Args:
            a (DocElement): The first point.
            b (DocElement): The second point.

        Returns:
            float: The Chebyshev distance between the two points.
        """
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        return max(dx, dy)

    @staticmethod
    def angle_inter_element(a: DocElement, b: DocElement) -> float:
        # TODO: angle relative to docuemnt Center
        """
        Compute the angle between two DocElements.

        Args:
            a (DocElement): The first DocElement.
            b (DocElement): The second DocElement.

        Returns:
            float: The angle between the two DocElements in radians.

        Note:
            The angle is calculated based on the centers of the bounding boxes
            of the DocElements.
        """
        # Compute center points
        center1 = (a.x + a.w / 2, a.y + a.h / 2)
        center2 = (b.x + b.w / 2, b.y + b.h / 2)

        # Compute differences
        dx = center2[0] - center1[0]
        dy = center2[1] - center1[1]

        # Compute and return the angle in radians
        return math.atan2(dy, dx)

    @staticmethod
    def calculate_overlap(a: DocElement, b: DocElement) -> float:
        """
        Calculate the degree of overlap between two bounding boxes.

        Args:
            a (DocElement): First bounding box.
            b (DocElement): Second bounding box.

        Returns:
            float: Degree of overlap between the bounding boxes.
        """
        # Calculate intersection coordinates
        x_left = max(a.x, b.x)
        y_top = max(a.y, b.y)
        x_right = min(a.x + a.w, b.x + b.w)
        y_bottom = min(a.y + a.h, b.y + b.h)

        # Calculate intersection area
        intersection_area = max(0, x_right - x_left) * max(0, y_bottom - y_top)

        # Calculate total area of smaller box
        total_area = min(a.w * a.h, b.w * b.h)

        # Calculate overlap ratio
        overlap_ratio = intersection_area / total_area if total_area > 0 else 0.0

        return overlap_ratio

    @staticmethod
    def calculate_horizontal_alignment(
        a: DocElement, b: DocElement
    ) -> HorizontalAlignment:
        """
        Calculate the horizontal alignment between two bounding boxes.

        Args:
            a (DocElement): The first bounding box.
            b (DocElement): The second bounding box.

        Returns:
            HorizontalAlignment: Horizontal alignment ('left', 'center', 'right').
        """
        x1, _, w1, _ = a.x, a.y, a.w, a.h
        x2, _, w2, _ = b.x, b.y, b.w, b.h

        if x1 == x2:
            return HorizontalAlignment.CENTER
        elif x1 < x2:
            if x1 + w1 == x2:
                return HorizontalAlignment.RIGHT
            else:
                return HorizontalAlignment.LEFT
        else:
            if x2 + w2 == x1:
                return HorizontalAlignment.LEFT
            else:
                return HorizontalAlignment.RIGHT

    @staticmethod
    def calculate_vertical_alignment(a: DocElement, b: DocElement) -> VerticalAlignment:
        """
        Calculate the vertical alignment between two bounding boxes.

        Args:
            a (DocElement): The first bounding box.
            b (DocElement): The second bounding box.

        Returns:
            VerticalAlignment: Vertical alignment ('top', 'middle', 'bottom').
        """
        _, y1, _, h1 = a.x, a.y, a.w, a.h
        _, y2, _, h2 = b.x, b.y, b.w, b.h

        if y1 == y2:
            return VerticalAlignment.MIDDLE
        elif y1 < y2:
            if y1 + h1 == y2:
                return VerticalAlignment.BOTTOM
            else:
                return VerticalAlignment.TOP
        else:
            if y2 + h2 == y1:
                return VerticalAlignment.TOP
            else:
                return VerticalAlignment.BOTTOM
