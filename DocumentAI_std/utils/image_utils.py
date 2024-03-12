# TODO: Gabor, Entropy and every Textural Image
# TODO: Add a library for Embedding (Visaul, Text, and combined)
from DocumentAI_std.base.doc_element import DocElement


class ImageUtils:
    def entropy(self, doc_element: DocElement) -> float:

        tensor = doc_element.extract_pixels()

        # Compute the probability distribution of values in the tensor
        probabilities = F.softmax(tensor.view(-1), dim=0)

        # Compute Shannon entropy
        entropy = -(probabilities * torch.log2(probabilities + 1e-10)).sum()