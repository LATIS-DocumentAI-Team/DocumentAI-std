from src.datasets.wildreceipt import Wildreceipt


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
