import json
import os
from pathlib import Path
from typing import List

from DocumentAI_std.base.document_entity_classification import (
    DocumentEntityClassification,
)

from DocumentAI_std.utils.base_utils import BaseUtils

from DocumentAI_std.base.document import Document


class CORD:
    # FIXME: CONVERT THIS TO X, Y, W, H

    """CORD dataset from `"CORD: A Consolidated Receipt Dataset forPost-OCR Parsing"
    <https://openreview.net/pdf?id=SJl3z659UH>`_.

    .. image:: https://github.com/mindee/doctr/releases/download/v0.5.0/cord-grid.png
        :align: center

    >>> from doctr.datasets import CORD
    >>> train_set = CORD(train=True, download=True)
    >>> img, target = train_set[0]

    Args:
        train: whether the subset should be the training one
        use_polygons: whether polygons should be considered as rotated bounding box (instead of straight ones)
        **kwargs: keyword arguments from `VisionDataset`.
    :return:
        Bounding boxes are in the Format (xmin, ymin, xmax, ymax) top left, bottom right corners
    """

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
        >>> dataset = CORD(
        ...     img_folder="/path/to/cord_train/image",
        ...     label_path="/path/to/cord_train/json",
        ...     train=True
        ... )
        >>> dataset = CORD(
        ...     img_folder="/path/to/cord_test/image",
        ...     label_path="/path/to/cord_test/json",
        ...     train=False
        ... )
        """

    TRAIN = (
        "https://github.com/mindee/doctr/releases/download/v0.1.1/cord_train.zip",
        "45f9dc77f126490f3e52d7cb4f70ef3c57e649ea86d19d862a2757c9c455d7f8",
    )

    TEST = (
        "https://github.com/mindee/doctr/releases/download/v0.1.1/cord_test.zip",
        "8c895e3d6f7e1161c5b7245e3723ce15c04d84be89eaa6093949b75a66fb3c58",
    )

    def __init__(
        self,
        img_folder: str,
        label_path: str,
        train: bool = True,
    ) -> None:
        if not os.path.exists(label_path) or not os.path.exists(img_folder):
            raise FileNotFoundError(
                f"unable to locate {label_path if not os.path.exists(label_path) else img_folder}"
            )

        tmp_root = img_folder
        self.train = train

        self.data: List[Document] = []

        for img_path in os.listdir(tmp_root):
            # File existence check
            if not os.path.exists(os.path.join(tmp_root, img_path)):
                raise FileNotFoundError(
                    f"unable to locate {os.path.join(tmp_root, img_path)}"
                )

            stem = Path(img_path).stem
            _targets = []

            with open(os.path.join(label_path, f"{stem}.json"), "rb") as f:
                label = json.load(f)
                row_id_dic = {}
                for line in label["valid_line"]:
                    # text_unit = ""

                    for word in line["words"]:
                        if len(word["text"]) > 0:
                            # text_unit += word["text"] + " "
                            # row_id_dic[word['row_id']] += word["text"] + " "
                            if word["row_id"] in row_id_dic:
                                row_id_dic[word["row_id"]] += word["text"].lower() + " "
                            else:
                                row_id_dic[word["row_id"]] = word["text"].lower() + " "
                            x = (
                                word["quad"]["x1"],
                                word["quad"]["x2"],
                                word["quad"]["x3"],
                                word["quad"]["x4"],
                            )
                            y = (
                                word["quad"]["y1"],
                                word["quad"]["y2"],
                                word["quad"]["y3"],
                                word["quad"]["y4"],
                            )
                            # Reduce 8 coords to 4 -> xmin, ymin, xmax, ymax
                            box = BaseUtils.X1X2_to_xywh(
                                [min(x), min(y), max(x), max(y)]
                            )
                            _targets.append((box, word["text"], line["category"]))

                if len(_targets) != 0:
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
        self.root = tmp_root
