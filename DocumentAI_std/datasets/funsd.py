
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
        ...     img_folder="/path/to/funsd/dataset/training_data/images",
        ...     label_path="/path/to/funsd/dataset/training_data/annotations",
        ...     train=True
        ... )
        >>> dataset = FUNSD(
        ...     img_folder="/path/to/funsd/dataset/testing_data/images",
        ...     label_path="/path/to/funsd/dataset/testing_data/annotations",
        ...     train=True
        ... )
        """

    URL = "https://guillaumejaume.github.io/FUNSD/dataset.zip"
    SHA256 = "c31735649e4f441bcbb4fd0f379574f7520b42286e80b01d80b445649d54761f"
    FILE_NAME = "funsd.zip"

    def __init__(
        self,
        img_folder: str,
        label_path: str,
        train: bool = True,
    ) -> None:

        self.train = train

        # Use the subset
        subfolder = os.path.join(
            "dataset", "training_data" if train else "testing_data"
        )

        # # List images
        tmp_root = os.path.join(self.root, subfolder, "images")

        self.data: List[Tuple[str, Dict[str, Any]]] = []
        for img_path in os.listdir(tmp_root):
            # File existence check
            if not os.path.exists(os.path.join(tmp_root, img_path)):
                raise FileNotFoundError(
                    f"unable to locate {os.path.join(tmp_root, img_path)}"
                )

            stem = Path(img_path).stem
            with open(
                os.path.join(self.root, subfolder, "annotations", f"{stem}.json"), "rb"
            ) as f:
                data = json.load(f)
            _targets = [
                (convert_xmin_ymin(block["box"]), block["text"].lower(), block["label"])
                for block in data["form"]
                if get_area(convert_xmin_ymin(block["box"])) >= 50
                or block["label"] in ["question", "answer", "other", "header"]
            ]

            # for each img_path,
            # data is the data of that image
            # data['form'] get the all data which is under 'form' key
            # data['form'][0] get the data under the first bbox
            if _targets:
                box_targets, text_units, labels = zip(*_targets)
                if (
                    len(box_targets) > 1
                ):  # number of bounding boxes in document should be more than one
                    self.data.append(
                        (
                            img_path,
                            dict(
                                boxes=np.asarray(box_targets, dtype=int),
                                text_units=list(text_units),
                                labels=list(labels),
                            ),
                        )
                    )
        self.root = tmp_root