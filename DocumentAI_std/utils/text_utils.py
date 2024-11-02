import json
import os
import re
import urllib
import zipfile
from typing import Optional

import requests
import spacy

from DocumentAI_std.base.doc_element import DocElement
from DocumentAI_std.base.doc_enum import ContentType


# TODO: - ADD strategy the compute text embeddings
#       - ADD methods and some logic related the image content of each doc element (develop a utils for it also)
#       - Write a document (.md file) explain the architecture and the relationship between classes and a develop guide
class TextUtils:

    city_country_cache = {}
    country_dict = {}
    geonames_url = "https://www.geonames.org/search.html"
    nlp = spacy.load("en_core_web_sm")

    @staticmethod
    def nbr_chars(doc_element: DocElement) -> int:
        """
        Count the number of characters in the content of a DocElement if it is of type TEXT.

        Args:
            (doc_element DocElement): The document element to count characters from.

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

    @staticmethod
    def is_zip_code(doc_element: DocElement) -> bool:
        """
        Determines if the content of a given DocElement represents a valid ZIP code,
        supporting Canadian postal codes, US ZIP codes, and 6-digit numeric codes.

        This method validates that the content type of the DocElement is TEXT and then
        checks whether the content matches a recognized ZIP code pattern.

        Args:
            doc_element (DocElement): The document element whose content is to be checked.

        Returns:
            bool: True if the content matches a valid ZIP code pattern, False otherwise.

        Raises:
            AssertionError: If the content type of the DocElement is not TEXT.

        Notes:
            - Supports Canadian postal codes in the format `A1A 1A1`.
            - Supports US ZIP codes in the formats `12345`, `12345-6789`.
            - Supports 6-digit numeric ZIP codes (e.g., `800010`).
        """
        # Verify content type is TEXT
        if doc_element.content_type != ContentType.TEXT:
            raise AssertionError("ZIP code check requires content type TEXT")

        text = doc_element.content.strip()

        # Define patterns for Canadian, US, and 6-digit numeric ZIP codes
        canadian_zip_code_pattern = r"\b([A-Z]\d[A-Z])\s*\d[A-Z]\d\b"
        us_zip_code_pattern = r"\b\d{5}(?:-\d{4})?\b"
        six_digit_zip_code_pattern = r"\b\d{6}\b"

        # Check if the content matches any of the ZIP code patterns
        return bool(
            re.fullmatch(canadian_zip_code_pattern, text)
            or re.fullmatch(us_zip_code_pattern, text)
            or re.fullmatch(six_digit_zip_code_pattern, text)
        )

    @staticmethod
    def extract_zip_code(text: str) -> Optional[str]:
        """
        Extracts the first occurrence of a ZIP code from a given text, supporting Canadian, US, and 6-digit formats.

        Args:
            text (str): The text from which to extract the ZIP code.

        Returns:
            Optional[str]: The first ZIP code found, or None if no valid ZIP code is present.

        Notes:
            - Supports Canadian postal codes in the format `A1A 1A1`.
            - Supports US ZIP codes in the formats `12345`, `12345-6789`.
            - Supports 6-digit numeric ZIP codes (e.g., `800010`).
        """
        zip_code_pattern = r"\b([A-Z]\d[A-Z]\s*\d[A-Z]\d|\d{5}(?:-\d{4})?|\d{6})\b"
        match = re.search(zip_code_pattern, text)
        return match.group(0) if match else None

    @staticmethod
    def is_url_reachable(url: str) -> bool:
        """Checks if the given URL is reachable."""
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            print(f"Warning: Unable to reach {url}")
            return False

    @staticmethod
    def is_known_city(doc_element: DocElement) -> bool:
        """
        Checks if the content of a given DocElement is a known city by querying the GeoNames service.

        Args:
            doc_element (DocElement): The document element containing the text to check.

        Returns:
            bool: True if the content matches a known city name, False otherwise.

        Raises:
            AssertionError: If the content type of the DocElement is not TEXT.
        """
        # Verify content type is TEXT
        if doc_element.content_type != ContentType.TEXT:
            raise AssertionError("City check requires content type TEXT")

        # Normalize city name (trim spaces, capitalize appropriately)
        city_name = doc_element.content.strip().title()

        # Check if the URL is reachable before making the query
        if not TextUtils.is_url_reachable(TextUtils.geonames_url):
            print("GeoNames service is currently unreachable.")
            return False

        # Check the cache first to avoid unnecessary requests
        if city_name in TextUtils.city_country_cache:
            return True

        try:
            # Query GeoNames for the city name
            response = requests.get(f"{TextUtils.geonames_url}?q={city_name}&country=")
            # Attempt to find the country in the response HTML
            if re.search(r"/countries/[A-Z]{2}/[a-zA-Z-]+\.html", response.text):
                # Cache the city as known if the country is found
                TextUtils.city_country_cache[city_name] = True
                return True
        except requests.RequestException:
            print(f"Warning: Could not verify city '{city_name}'")

        # If no match found, return False
        return False

    @classmethod
    def load_countries(cls):
        """
        Load country data from a JSON file and make both keys and values lowercase.
        """
        try:
            base_dir = os.path.dirname(__file__)  # Directory of the TextUtils module
            json_file_path = os.path.join(
                base_dir, "countries.json"
            )  # Construct the path

            with open(json_file_path, "r") as f:
                data = json.load(f)
                cls.country_dict = {
                    k.lower(): v.lower() if isinstance(v, str) else v
                    for k, v in data.items()
                }
        except FileNotFoundError:
            print("Error: countries.json file not found.")
        except json.JSONDecodeError:
            print("Error: Failed to decode countries.json.")

    @staticmethod
    def is_known_country(doc_element: DocElement) -> bool:
        """
        Checks if the content of a given DocElement matches a known country code or name.

        Args:
            doc_element (DocElement): The document element containing the text to check.

        Returns:
            bool: True if the content matches a known country name or code, False otherwise.

        Raises:
            AssertionError: If the content type of the DocElement is not TEXT.
        """
        # Verify content type is TEXT
        TextUtils.load_countries()
        if doc_element.content_type != ContentType.TEXT:
            raise AssertionError("Country check requires content type TEXT")

        # Normalize the country name or code by stripping spaces and converting to lowercase
        country_text = doc_element.content.lower()
        # Check if the text matches a known country name or code
        if (
            country_text in TextUtils.country_dict.values()
            or country_text in TextUtils.country_dict.keys()
        ):
            return True

        # If no match is found, return False
        return False

    @staticmethod
    def is_person_name(doc_element: DocElement) -> bool:
        """
        Determines if the content of a given `DocElement` instance is classified as a person's name.

        Args:
            doc_element (DocElement): An instance of `DocElement` containing the text to evaluate.

        Returns:
            bool: True if the entire text is classified as a person’s name based on named entity recognition, False otherwise.

        Example:
            >>> doc_element = DocElement(0, 0, 0, 0, ContentType.TEXT, 'John Doe')
            >>> TextUtils.is_person_name(doc_element)
            True
        """
        text = doc_element.content.lower()
        doc = TextUtils.nlp(text)

        # Check for named entities in the processed text
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return True
        return False

    @staticmethod
    def person_name_probability(doc_element: DocElement) -> float:
        """
        Calculates the probability that the content of a `DocElement` instance is classified as a person’s name.

        Args:
            doc_element (DocElement): An instance of `DocElement` containing the text to evaluate.

        Returns:
            float: The probability, ranging from 0.0 to 1.0, that the text is classified as a person’s name.
                   If no entities are found, returns 0.0.

        Example:
            >>> doc_element = DocElement(0, 0, 0, 0, ContentType.TEXT, 'Alice Johnson')
            >>> TextUtils.person_name_probability(doc_element)
            1.0
        """
        text = doc_element.content.lower()
        doc = TextUtils.nlp(text)

        # Count the number of person entities and total entities
        person_count = sum(1 for ent in doc.ents if ent.label_ == "PERSON")
        total_count = len(doc.ents)

        # Calculate probability
        if total_count > 0:
            probability = person_count / total_count
        else:
            probability = 0.0  # No entities found

        return probability

    @staticmethod
    def is_real_number(doc_element: DocElement) -> bool:
        """
        Determines if the content of a `DocElement` instance represents a real number, supporting both integer and decimal formats.

        Args:
            doc_element (DocElement): An instance of `DocElement` containing the text to evaluate.

        Returns:
            bool: True if the content is a valid real number, False otherwise.

        Example:
            >>> doc_element = DocElement(0, 0, 0, 0, ContentType.TEXT, '123.45')
            >>> TextUtils.is_real_number(doc_element)
            True
        """
        text = doc_element.content
        pattern = r"^-?\d+(\.\d+)?$"
        return bool(re.match(pattern, text))

    @staticmethod
    def is_currency(doc_element: DocElement) -> bool:
        """
        Checks if the content of a `DocElement` instance represents a currency amount.

        Args:
            doc_element (DocElement): An instance of `DocElement` containing the text to evaluate.

        Returns:
            bool: True if the content matches a currency format, False otherwise.

        Supported Formats:
            - Matches various world currencies, including symbols (e.g., $, €, ¥, £) and abbreviations (e.g., TND, AED, SAR).
            - Accepts amounts in formats like "$123.45", "€99", "100 TND".

        Example:
            >>> doc_element = DocElement(0, 0, 0, 0, ContentType.TEXT, '$123.45')
            >>> TextUtils.is_currency(doc_element)
            True
        """
        text = doc_element.content
        pattern = r'^(?:(?:[¥€$£₹₩₺₽د.تد.إد.م.تد.ج]?\d+(\.\d{2})?)|\d+(\.\d{2})?\s?(TND|AED|SAR|EGP|KWD|QAR|BHD|OMR|¥|€|$|£|₹|₩|₺|₽|د.ت|د.إ|ر.س|ج.م|د.ك|ر.ق|د.ب|ر.ع.|د.ج|د.م))$'
        return bool(re.match(pattern, text))

    @staticmethod
    def has_real_and_currency(doc_element: DocElement) -> bool:
        """
        Checks if the content of a `DocElement` instance represents both a real number and a currency format.

        Args:
            doc_element (DocElement): An instance of `DocElement` containing the text to evaluate.

        Returns:
            bool: True if the content matches both a real number and a currency format, False otherwise.

        Example:
            >>> doc_element = DocElement(0, 0, 0, 0, ContentType.TEXT, '$123.45')
            >>> TextUtils.has_real_and_currency(doc_element)
            True
        """
        text = doc_element.content
        return TextUtils.is_real_number(doc_element) and TextUtils.is_currency(
            doc_element
        )
