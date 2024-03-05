import re

from DocumentAI_std.base.doc_element import DocElement
from DocumentAI_std.base.doc_enum import ContentType


# TODO: - ADD strategy the compute text embeddings
#       - ADD methods and some logic related the image content of each doc element (develop a utils for it also)
#       - Write a document (.md file) explain the architecture and the relationship between classes and a develop guide
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
            raise AssertionError(
                "Cannot check for special characters in non-TEXT objects"
            )

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
            raise AssertionError(
                "Cannot calculate numeric percentage in non-TEXT objects"
            )

        # Initialize count for numeric characters and total characters
        num_numeric_chars = sum(1 for char in doc_element.content if char.isdigit())
        total_chars = len(doc_element.content)

        # Calculate the percentage
        if total_chars == 0:
            return 0.0
        else:
            return num_numeric_chars / total_chars

    @staticmethod
    def is_date(doc_element: DocElement) -> bool:
        """
        Check if the given text contains a date in various formats.

        Args:
            doc_element (DocElement): The document element to check for a date.

        Returns:
            bool: True if the text contains a date, False otherwise.

        Raises:
            AssertionError: If the content type of the DocElement is not TEXT.
        """
        # Ensure the content type is TEXT
        if doc_element.content_type != ContentType.TEXT:
            raise AssertionError(
                "Cannot calculate numeric percentage in non-TEXT objects"
            )
        text = doc_element.content
        # Define regular expression patterns for different date formats
        date_patterns = [
            r"\b(\d{1,2}/\d{1,2}/\d{4})\b",  # dd/mm/yyyy
            r"\b(\d{1,2}-\d{1,2}-\d{4})\b",  # dd-mm-yyyy
            r"\b(\d{1,2}\s\w+\s\d{4})\b",  # dd month yyyy
            r"\b(\d{1,2}\s\w{3,}\s\d{4})\b",  # month dd yyyy
            r"\b(\w{3,}\s\d{1,2}\s\d{4})\b",  # month day yyyy
            r"\b(\w{3,}\,\s\d{1,2}\s\d{4})\b",  # month, day yyyy
            r"\b(\d{1,2}\|\d{1,2}\|\d{4})\b",  # dd|mm|yyyy
            r"\b(\d{1,2}-\d{1,2}-\d{4})\b",  # mm-dd-yyyy
            r"\b(\d{1,2}/\d{1,2}/\d{4})\b",  # mm/dd/yyyy
            r"\b(\d{1,2}\s\w+\s\d{1,2}\s\d{4})\b",  # dd month dd yyyy
            r"\b(\w{3,}\s\d{1,2}\s\w{3,}\s\d{4})\b",  # month dd month yyyy
            r"\b(\w{3,}\,\s\d{1,2}\s\w{3,}\s\d{4})\b",  # month, dd month yyyy
            r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s(\d{1,2})\s(\w{3,})\s(\d{4})\b",
            # Monday 15 July 2023
            r"\b(\w{3,}\s\d{1,2},\s\d{4})\b",  # Month dd, yyyy (e.g., March 12, 2023)
        ]

        # Check each pattern for a match in the text
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return True

        return False

    @staticmethod
    def levenshtein_distance(a: DocElement, b: DocElement) -> int:
        """
        Compute the Levenshtein distance between the content of two DocElements.

        Args:
            a (DocElement): The first DocElement.
            b (DocElement): The second DocElement.

        Returns:
            int: The Levenshtein distance between the content of the two DocElements.

        Raises:
            AssertionError: If either of the DocElements does not contain text content.
        """
        if a.content_type != ContentType.TEXT or b.content_type != ContentType.TEXT:
            raise AssertionError(
                "Cannot calculate Levenshtein distance for non-text content"
            )

        s1, s2 = a.content, b.content

        # Ensure s1 is the shorter string
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        # Initialize the previous and current rows of the matrix
        prev_row = list(range(len(s2) + 1))
        curr_row = [0] * (len(s2) + 1)

        # Compute the Levenshtein distance row by row
        for i in range(1, len(s1) + 1):
            curr_row[0] = i
            for j in range(1, len(s2) + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                curr_row[j] = min(
                    curr_row[j - 1] + 1,  # Insertion
                    prev_row[j] + 1,  # Deletion
                    prev_row[j - 1] + cost,  # Substitution
                )
            prev_row, curr_row = curr_row, prev_row

        return prev_row[-1]
