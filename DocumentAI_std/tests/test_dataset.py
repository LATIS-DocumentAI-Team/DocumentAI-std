from DocumentAI_std.datasets.wildreceipt import Wildreceipt
from DocumentAI_std.datasets.cord import CORD


class TestDataset:
    def test_wildreceipt_dataset(self):
        train_set = Wildreceipt(
            train=True,
            img_folder="/home/bobmarley/PycharmProjects/DocumentAI-std/data/wildreceipt/",
            label_path="/home/bobmarley/PycharmProjects/DocumentAI-std/data/wildreceipt/train.txt",
        )
        test_set = Wildreceipt(
            train=False,
            img_folder="/home/bobmarley/PycharmProjects/DocumentAI-std/data/wildreceipt/",
            label_path="/home/bobmarley/PycharmProjects/DocumentAI-std/data/wildreceipt/test.txt",
        )
        assert len(train_set.data) == 1267
        assert len(test_set.data) == 472

    def test_cord_dataset(self):
        train_set = CORD(
            train=True,
            img_folder="/home/bobmarley/.cache/doctr/datasets/cord_train/image",
            label_path="/home/bobmarley/.cache/doctr/datasets/cord_train/json",
        )
        test_set = CORD(
            train=False,
            img_folder="/home/bobmarley/.cache/doctr/datasets/cord_test/image",
            label_path="/home/bobmarley/.cache/doctr/datasets/cord_test/json",
        )
        assert len(train_set.data) == 800
        assert len(test_set.data) == 100
