import os
from typing import Any


class Document:
    """
    The class describe a document by its content, a document in our case is defined by:
        file_name: str
        bounding boxes: List[List]
        content: content of each bounding box : List
        content_type: type of each bounding box content: Enum.ContentType

    :arg
        ---
        img_path: path to document
        ocr_output: define the output of an ocr, (here we assume it is a json format in the following format)
        {
            bbox: List[List]
            content: List[Any]
        }
        this output are generate from an ocr engine
        ---
    """
    # TODO: Create a Adapter class which adapt from Paddle to ocr_output, from EasyOcr to

    # TODO: - ASK how to create a Document (normaly a list of docElements)
    #       - The problem is how to check the type of the content ?
    #       - Else we do not create class for document
    def __init__(self, img_path: str, ocr_output: dict, **kwargs: Any) -> None:
        # File existence check
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"unable to locate img_folder at {img_path}")

        filename = os.path.basename(img_path)


        pass