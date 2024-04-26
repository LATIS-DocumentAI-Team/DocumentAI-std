import json
import os
from pathlib import Path
from typing import List

from DocumentAI_std.base.document_entity_classification import (
    DocumentEntityClassification,
)

from DocumentAI_std.utils.base_utils import BaseUtils

from DocumentAI_std.base.document import Document


class FUNSD:
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
    >>> dataset = FUNSD(
    ...     data_folder="/path/to/funsd/"
    ...     train=True
    ... )
    """

    def __init__(
        self,
        data_folder: str,
        train: bool = True,
    ) -> None:
        self.train = train
        self.root = data_folder
        # Use the subset
        sub_folder = os.path.join(
            "dataset", "training_data" if train else "testing_data"
        )

        # # List images
        tmp_root = os.path.join(self.root, sub_folder, "images")
        self.data: List[Document] = []

        for img_path in os.listdir(tmp_root):
            # File existence check
            if not os.path.exists(os.path.join(tmp_root, img_path)):
                raise FileNotFoundError(
                    f"unable to locate {os.path.join(tmp_root, img_path)}"
                )

            stem = Path(img_path).stem
            with open(
                os.path.join(self.root, sub_folder, "annotations", f"{stem}.json"), "rb"
            ) as f:
                data = json.load(f)
            _targets = [
                (BaseUtils.X1X2_to_xywh(block["box"]), block["text"], block["label"])
                for block in data["form"]
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
                        os.path.join(tmp_root, img_path), ocr_output
                    )
                )
