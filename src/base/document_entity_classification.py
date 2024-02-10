from typing import Any

from src.base.document import Document


class DocumentEntityClassification(Document):
    def __init__(self, img_path: str, ocr_output: dict, **kwargs: Any) -> None:
        super.__init__(img_path, ocr_output, **kwargs)
        pass
