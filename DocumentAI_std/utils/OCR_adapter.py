import io
from typing import Union, List

import easyocr
import numpy as np
import pytesseract
from PIL import Image
from paddleocr import PaddleOCR

from DocumentAI_std.utils.base_utils import BaseUtils
from DocumentAI_std.base.document import Document


class OCRAdapter:
    """
    Adapter class for standardizing OCR outputs from various engines.

    This class provides a centralized interface to convert OCR results obtained
    from different OCR engines, such as PaddleOCR, EasyOCR, and Tesseract, into
    a uniform and consistent format. The standardized format ensures ease of
    handling, processing, and further analysis of OCR data across different engines.

    Attributes:
        ocr_method (str): The OCR method currently set for processing.
        lang (List[str]): The language(s) specified for OCR processing.

    Methods:
        __init__(ocr_method: str, lang: List[str]): Initialize the OCRAdapter instance with the specified OCR method and language settings.
        apply_ocr(source: Union[str, io.BytesIO]) -> Document: Apply OCR to the given source using the specified OCR method.
        apply_easyocr(source: Union[str, io.BytesIO]) -> dict: Apply OCR using EasyOCR.
        apply_paddleocr(source: Union[str, io.BytesIO]) -> dict: Apply OCR using PaddleOCR.
        apply_tesseract_ocr(source: Union[str, io.BytesIO]) -> dict: Apply OCR using Tesseract.
        from_paddle_ocr(paddle_ocr_output): Convert PaddleOCR output to a standardized format.
        from_easy_ocr(easy_ocr_output): Convert EasyOCR output to a standardized format.
        from_tesseract_ocr(tesseract_ocr_output): Convert Tesseract OCR output to a standardized format.
    """

    def __init__(self, ocr_method: str, lang: List[str]):
        """
        Initialize the OCRAdapter instance with the specified OCR method and language settings.

        Args:
            ocr_method (str): The OCR method to be used for processing.
                Supported methods include "easyocr", "paddle", and "tesseract".
            lang (List[str]): A list of language codes specifying the language(s) to be used for OCR.
                Example: ["en", "fr"] for English and French.
        """
        self.__ocr_method = ocr_method
        self.lang = lang

    @property
    def ocr_method(self):
        return self.__ocr_method

    @ocr_method.setter
    def ocr_method(self, value):
        self.__ocr_method = value

    def apply_ocr(self, source: Union[str, io.BytesIO]) -> Document:
        """
        Apply OCR to the given source using the specified OCR method.

        Args:
            source (Union[str, io.BytesIO]): The source of the image file to apply OCR on.

        Returns:
            Document: A Document object containing the source and OCR result.

        Raises:
            AssertionError: If the specified OCR method is not recognized.
        """
        ocr_methods = {
            "easy": self.apply_easy_ocr,
            "paddle": self.apply_paddleocr,
            "tesseract": self.apply_tesseract_ocr,
        }
        # TODO: Remove BytesIO, accept only Path
        if self.ocr_method not in ocr_methods:
            raise AssertionError(f"OCR method '{self.ocr_method}' is not recognized.")

        result = ocr_methods[self.ocr_method](source)
        return Document(source, result)

    def apply_easy_ocr(self, source: Union[str, io.BytesIO]) -> dict:
        """
        Apply OCR using EasyOCR.

        Args:
            source (Union[str, io.BytesIO]): The source of the image file to apply OCR on.

        Returns:
            dict: OCR result.
        """
        reader = easyocr.Reader(self.lang)
        return OCRAdapter.from_easy_ocr(reader.readtext(source))

    def apply_paddleocr(self, source: Union[str, io.BytesIO]) -> dict:
        """
        Apply OCR using PaddleOCR.

        Args:
            source (Union[str, io.BytesIO]): The source of the image file to apply OCR on.

        Returns:
            dict: OCR result.
        """
        im = self._open_image(source)
        lang_map = {
            "fr": "french",
            "en": "en",
            "de": "german",
            "ar": "ar",
            "ja": "japan",
            "ch_sim": "ch",
            "hi": "hi",
        }
        ocr = PaddleOCR(
            lang=lang_map[self.lang[0]],
        )
        return OCRAdapter.from_paddle_ocr(ocr.predict(np.asarray(im)))

    def apply_tesseract_ocr(self, source: Union[str, io.BytesIO]) -> dict:
        """
        Apply OCR using Tesseract.

        Args:
            source (Union[str, io.BytesIO]): The source of the image file to apply OCR on.

        Returns:
            dict: OCR result.
        """
        im = self._open_image(source)
        lang_map = {
            "fr": "fra",
            "en": "eng",
            "de": "deu",
            "ar": "ara",
            "ja": "jpn",
            "ch_sim": "chi_sim",
            "hi": "hin",
        }
        lang = "+".join([lang_map[key] for key in self.lang])
        return OCRAdapter.from_tesseract_ocr(
            pytesseract.image_to_data(
                im,
                lang=lang,
                output_type=pytesseract.Output.DICT,
            )
        )

    @staticmethod
    def _open_image(source: Union[str, io.BytesIO]) -> Image.Image:
        """
        Open and convert the image file to RGB format.

        Args:
            source (Union[str, io.BytesIO]): The source of the image file.

        Returns:
            Image.Image: Image object in RGB format.
        """
        im = Image.open(source)
        return im.convert("RGB")

    @staticmethod
    def from_paddle_ocr(paddle_ocr_output):
        """
        Convert PaddleOCR output to a standardized format.

        Args:
            paddle_ocr_output (list): List containing OCR output from PaddleOCR engine
                                      or mock dictionaries with 'rec_boxes' and 'rec_res'.

        Returns:
            dict: Dictionary containing standardized OCR output with 'bbox' and 'content' keys.
        """
        bbox_content_pairs = []

        for output in paddle_ocr_output:
            if isinstance(output, dict):
                # Handle mock dictionary with 'rec_boxes' and 'rec_res'
                rec_boxes = output.get("rec_boxes", [])
                rec_res = output.get("rec_res", [["", 0.0]] * len(rec_boxes))
                for box, res in zip(rec_boxes, rec_res):
                    bbox_content_pairs.append((BaseUtils.X1X2_to_xywh(box), res[0]))
            elif isinstance(output, list):
                # Handle real PaddleOCR output (list of tuples)
                for box, res in output:
                    bbox_content_pairs.append((BaseUtils.X1X2_to_xywh(box), res[0]))
            else:
                raise TypeError(
                    f"Unsupported paddle_ocr_output element: {type(output)}"
                )

        if bbox_content_pairs:
            bbox, content = zip(*bbox_content_pairs)
        else:
            bbox, content = [], []

        return {"bbox": list(bbox), "content": list(content)}

    @staticmethod
    def from_easy_ocr(easy_ocr_output):
        """
        Convert EasyOCR output to a standardized format.

        Args:
            easy_ocr_output (list): List containing OCR output from EasyOCR engine.

        Returns:
            dict: Dictionary containing standardized OCR output with 'bbox' and 'content' keys.
        """
        bbox_content_pairs = [
            (
                list(map(int, BaseUtils.X1X2X3X4_to_xywh(sum(text_box[0], [])))),
                text_box[1],
            )
            for text_box in easy_ocr_output
        ]

        bbox, content = zip(*bbox_content_pairs)

        return {"bbox": list(bbox), "content": list(content)}

    @staticmethod
    def from_tesseract_ocr(tesseract_ocr_output):
        """
        Convert Tesseract OCR output to a standardized format.

        Args:
            tesseract_ocr_output (dict): Dictionary containing OCR output from Tesseract engine.

        Returns:
            dict: Dictionary containing standardized OCR output with 'bbox' and 'content' keys.
        """
        bbox_content_pairs = [
            (
                [
                    int(tesseract_ocr_output["left"][i]),
                    int(tesseract_ocr_output["top"][i]),
                    int(tesseract_ocr_output["width"][i]),
                    int(tesseract_ocr_output["height"][i]),
                ],
                tesseract_ocr_output["text"][i],
            )
            for i in range(len(tesseract_ocr_output["text"]))
            if int(tesseract_ocr_output["conf"][i]) > 0
        ]

        bbox, content = zip(*bbox_content_pairs)
        return {"bbox": list(bbox), "content": list(content)}
