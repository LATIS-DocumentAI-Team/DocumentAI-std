import json
import os
from typing import List

from DocumentAI_std.base.document_entity_classification import DocumentEntityClassification

from DocumentAI_std.utils.base_utils import BaseUtils

from DocumentAI_std.base.document import Document


class XFUND:
    """
    CORD dataset from `"CORD: A Consolidated Receipt Dataset forPost-OCR Parsing"
    <https://openreview.net/pdf?id=SJl3z659UH>`_.



    Args:
        img_folder (str): Folder containing all the images of the dataset.
        label_path (str): Path to the annotations file of the dataset.
        train (bool, optional): Whether the subset should be the training one. Defaults to True.

    Attributes:
        data (List[DocumentEntityClassification]): List of document entities in the dataset.
        root (str): Root directory of the document image files.
        train (bool): Indicates whether the dataset is for training or not.

    Example:
    >>> dataset = XFUND(
    ...     data_folder="/path/to/xfund/"
    ...     train=True
    ... )
    """

    def __init__(
        self,
        data_folder: str,
        train: bool = True,
    ) -> None:
        # File existence check
        if not os.path.exists(data_folder):
            raise FileNotFoundError(f"unable to locate {data_folder}")

        self.train = train
        self.data: List[Document] = []
        tmp_root = os.path.join(
            data_folder, "en.train.json" if train else "en.val.json"
        )
        with open(tmp_root, "r") as file:
            data = file.read()
        # Split the text file into separate JSON strings
        _targets = []
        json_data = json.loads(data)
        for document in json_data["documents"]:
            file_name = document["img"]["fname"]
            annotations = document["document"]
            _targets = [
                (
                    BaseUtils.X1X2_to_xywh(annotation["box"]),
                    annotation["text"],
                    annotation["label"],
                )
                for annotation in annotations
            ]
            if _targets:
                box_targets, text_targets, label_targets = zip(*_targets)
                ocr_output = {
                    "bbox": box_targets,
                    "content": text_targets,
                    "label": label_targets,
                }
                self.data.append(
                    DocumentEntityClassification(
                        os.path.join(data_folder, file_name), ocr_output
                    )
                )
        self.root = tmp_root
