import os
from typing import Any, List, Union, Tuple

from src.base.document import Document


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
            use_polygons: bool = False,
            recognition_task: bool = False,
            **kwargs: Any,
    ) -> None:

        # File existence check
        if not os.path.exists(label_path) or not os.path.exists(img_folder):
            raise FileNotFoundError(f"unable to locate {label_path if not os.path.exists(label_path) else img_folder}")

        tmp_root = img_folder
        self.train = train
        np_dtype = np.float32
        self.data: List[Tuple[Union[str, Document]]] = []

        with open(label_path, "r") as file:
            data = file.read()
        # Split the text file into separate JSON strings
        json_strings = data.strip().split("\n")
        box: Union[List[float], np.ndarray]
        _targets = []
        for json_string in json_strings:
            json_data = json.loads(json_string)
            img_path = json_data["file_name"]
            annotations = json_data["annotations"]
            for annotation in annotations:
                coordinates = annotation["box"]
                if use_polygons:
                    # (x, y) coordinates of top left, top right, bottom right, bottom left corners
                    box = np.array(
                        [
                            [coordinates[0], coordinates[1]],
                            [coordinates[2], coordinates[3]],
                            [coordinates[4], coordinates[5]],
                            [coordinates[6], coordinates[7]],
                        ],
                        dtype=np_dtype,
                    )
                else:
                    x, y = coordinates[::2], coordinates[1::2]
                    box = [min(x), min(y), max(x), max(y)]
                _targets.append((annotation["text"], box))
            text_targets, box_targets = zip(*_targets)

            if recognition_task:
                crops = crop_bboxes_from_image(
                    img_path=os.path.join(tmp_root, img_path), geoms=np.asarray(box_targets, dtype=int).clip(min=0)
                )
                for crop, label in zip(crops, list(text_targets)):
                    if label and " " not in label:
                        self.data.append((crop, label))
            else:
                self.data.append((
                    img_path,
                    dict(boxes=np.asarray(box_targets, dtype=int).clip(min=0), labels=list(text_targets)),
                ))
        self.root = tmp_root

    def extra_repr(self) -> str:
        return f"train={self.train}"
