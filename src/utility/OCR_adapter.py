from src.utility.base_utils import BaseUtils


class OCRAdapter:
    @staticmethod
    def from_paddle_ocr(paddle_ocr_output):
        for output in paddle_ocr_output:
            for text_box in output:
                print("j")
                print(text_box[0])
                # TODO: Convert text_box to the expected format of the mapper
                K = BaseUtils.x1y1x2y2x3y3x4y4_to_xywh(text_box[0])
                print("K")
                print(K)

    @staticmethod
    def from_easy_ocr(easy_ocr_output):
        pass
    @staticmethod
    def from_tesseract_ocr(tesseract_ocr_output):
        pass

