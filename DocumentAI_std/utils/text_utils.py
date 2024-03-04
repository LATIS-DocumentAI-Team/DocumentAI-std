from DocumentAI_std.base.content_type import ContentType

from DocumentAI_std.base.doc_element import DocElement


class TextUtils:
    @staticmethod
    def nbr_chars(doc_element: DocElement) -> int:
        """
        Count the number of characters in the content of a DocElement if it is of type TEXT.

        Args:
            doc_element (DocElement): The document element to count characters from.

        Returns:
            int: The number of characters in the content of the DocElement.

        Raises:
            AssertionError: If the content type of the DocElement is not TEXT.
        """
        if doc_element.content_type != ContentType.TEXT:
            raise AssertionError(
                "Cannot count the number of character of non TEXT Objects"
            )
        return len(doc_element.content)

    @staticmethod
    def has_special_char(doc_element: DocElement) -> bool:
        """
        Check if the content of a DocElement of type TEXT contains special characters.

        Args:
            doc_element (DocElement): The document element to check for special characters.

        Returns:
            bool: True if the content contains special characters, False otherwise.

        Raises:
            AssertionError: If the content type of the DocElement is not TEXT.
        """
        if doc_element.content_type != ContentType.TEXT:
            raise AssertionError("Cannot check for special characters in non-TEXT objects")

        special_chars = set("!@#$%^&*()_+{}[];:'\"<>,.?/\\|-")

        for char in doc_element.content:
            if char in special_chars:
                return True

        return False

    @staticmethod
    def count_special_chars(doc_element: DocElement) -> int:
        """
        Count the number of special characters in the content of a DocElement of type TEXT.

        Args:
            doc_element (DocElement): The document element to count special characters.

        Returns:
            int: The number of special characters in the content.

        Raises:
            AssertionError: If the content type of the DocElement is not TEXT.
        """
        if doc_element.content_type != ContentType.TEXT:
            raise AssertionError("Cannot count special characters in non-TEXT objects")

        special_chars = "!@#$%^&*()_+{}[];:'\"<>,.?/\\|-"
        return sum(1 for char in doc_element.content if char in special_chars)

    @staticmethod
    def calculate_numeric_percentage(doc_element: DocElement) -> float:
        """
        Calculate the percentage of numeric characters in the content of a DocElement of type TEXT.

        Args:
            doc_element (DocElement): The document element whose content's numeric percentage needs to be calculated.

        Returns:
            float: The percentage of numeric characters in the content.

        Raises:
            AssertionError: If the content type of the DocElement is not TEXT.
        """
        # Ensure the content type is TEXT
        if doc_element.content_type != ContentType.TEXT:
            raise AssertionError("Cannot calculate numeric percentage in non-TEXT objects")

        # Initialize count for numeric characters and total characters
        num_numeric_chars = sum(1 for char in doc_element.content if char.isdigit())
        total_chars = len(doc_element.content)

        # Calculate the percentage
        if total_chars == 0:
            return 0.0
        else:
            return num_numeric_chars / total_chars