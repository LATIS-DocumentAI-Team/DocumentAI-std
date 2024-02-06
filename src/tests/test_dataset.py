from src.datasets.wildreceipt import Wildreceipt


class TestDataset:
    def test_wildreceipt_dataset(self):
        train_set = Wildreceipt(train=True, img_folder="/home/bobmarley/PycharmProjects/DocumentAI-std/data/wildreceipt/",label_path = "/home/bobmarley/PycharmProjects/DocumentAI-std/data/wildreceipt/train.txt")
        train_set.data