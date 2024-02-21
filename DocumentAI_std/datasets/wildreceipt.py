import json
import os
from typing import List

from DocumentAI_std.base.document_entity_classification import (
    DocumentEntityClassification,
)

from DocumentAI_std.utils.base_utils import BaseUtils

from DocumentAI_std.base.document import Document


class Wildreceipt:
    """
    WildReceipt dataset from "Spatial Dual-Modality Graph Reasoning for Key Information Extraction"
    (https://arxiv.org/abs/2103.14470v1) and available at the following repository:
    https://download.openmmlab.com/mmocr/data/wildreceipt.tar.


    Args:
        img_folder (str): Folder containing all the images of the dataset.
        label_path (str): Path to the annotations file of the dataset.
        train (bool, optional): Whether the subset should be the training one. Defaults to True.

    Attributes:
        data (List[DocumentEntityClassification]): List of document entities in the dataset.
        root (str): Root directory of the document image files.
        train (bool): Indicates whether the dataset is for training or not.

    Example:
    >>> dataset = Wildreceipt(
    ...     img_folder="/path/to/images",
    ...     label_path="/path/to/annotations.json",
    ...     train=True
    ... )
    """

    def __init__(
        self,
        img_folder: str,
        label_path: str,
        train: bool = True,
    ) -> None:
        # File existence check
        if not os.path.exists(label_path) or not os.path.exists(img_folder):
            raise FileNotFoundError(
                f"unable to locate {label_path if not os.path.exists(label_path) else img_folder}"
            )

        tmp_root = img_folder
        self.train = train
        self.data: List[Document] = []

        with open(label_path, "r") as file:
            data = file.read()
        # Split the text file into separate JSON strings
        json_strings = data.strip().split("\n")
        _targets = []
        for json_string in json_strings:
            json_data = json.loads(json_string)
            img_path = json_data["file_name"]
            annotations = json_data["annotations"]

            box_targets, text_targets, label_targets = zip(
                *[
                    (
                        BaseUtils.X1X2X3X4_to_xywh(annotation["box"]),
                        annotation["text"].lower(),
                        annotation["label"],
                    )
                    for annotation in annotations
                ]
            )

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
        self.root = tmp_root
