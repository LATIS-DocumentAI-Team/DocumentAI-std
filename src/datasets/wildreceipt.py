import json
import os
from typing import List

from src.base.content_type import ContentType
from src.base.document import Document
from src.base.document_entity_classification import DocumentEntityClassification
from src.utility.base_utils import BaseUtils


# TODO: USE document Element Classififcation
class Wildreceipt:
    """WildReceipt dataset from `"Spatial Dual-Modality Graph Reasoning for Key Information Extraction"
        <https://arxiv.org/abs/2103.14470v1>`_ |
    `repository <https://download.openmmlab.com/mmocr/data/wildreceipt.tar>`_.

    .. image:: https://doctr-static.mindee.com/models?id=v0.7.0/wildreceipt-dataset.jpg&src=0
        :align: center


    Args:
    ----
        img_folder: folder with all the images of the dataset
        label_path: path to the annotations file of the dataset
        train: whether the subset should be the training one
        use_polygons: whether polygons should be considered as rotated bounding box (instead of straight ones)
        recognition_task: whether the dataset should be used for recognition task
        **kwargs: keyword arguments from `AbstractDataset`.
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
