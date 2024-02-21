from DocumentAI_std.utils.base_utils import BaseUtils


class OCRAdapter:
    """
    Adapter class for converting OCR outputs from different engines to a standardized format.

    The class provides static methods for converting OCR outputs from various engines
    (such as PaddleOCR, EasyOCR, and Tesseract) to a common format containing bounding boxes
    and corresponding content.

    Attributes:
        No attributes.

    Methods:
        from_paddle_ocr(paddle_ocr_output): Converts PaddleOCR output to standardized format.
        from_easy_ocr(easy_ocr_output): Converts EasyOCR output to standardized format.
        from_tesseract_ocr(tesseract_ocr_output): Converts Tesseract OCR output to standardized format.

    Expected Output Format:
        The expected output format after adaptation:
        {
            'bbox': List[List],
            'content': List[Any]
        }
    """

    @staticmethod
    def from_paddle_ocr(paddle_ocr_output):
        """
        Convert PaddleOCR output to a standardized format.

        Args:
            paddle_ocr_output (list): List containing OCR output from PaddleOCR engine.

        Returns:
            dict: Dictionary containing standardized OCR output with 'bbox' and 'content' keys.
        """
        bbox_content_pairs = [
            (BaseUtils.X1X2X3X4_to_xywh(sum(text_box[0], [])), text_box[1][0])
            for output in paddle_ocr_output
            for text_box in output
        ]

        bbox, content = zip(*bbox_content_pairs)

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
            (BaseUtils.X1X2X3X4_to_xywh(sum(text_box[0], [])), text_box[1])
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
