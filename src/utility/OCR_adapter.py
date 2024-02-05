import logging

from src.utility.base_utils import BaseUtils


class OCRAdapter:
    """
            output = {
            bbox: List[List]
            content: List[Any]
        }
    """
    @staticmethod
    def from_paddle_ocr(paddle_ocr_output):
        bbox_content_pairs = [
            (BaseUtils.X1X2X3X4_to_xywh(sum(text_box[0], [])), text_box[1][0])
            for output in paddle_ocr_output
            for text_box in output
        ]

        bbox, content = zip(*bbox_content_pairs)

        return {
            "bbox": list(bbox),
            "content": list(content)
        }

    @staticmethod
    def from_easy_ocr(easy_ocr_output):
        pass
    @staticmethod
    def from_tesseract_ocr(tesseract_ocr_output):
        pass

