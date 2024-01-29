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

    def __init__(self):
        pass
