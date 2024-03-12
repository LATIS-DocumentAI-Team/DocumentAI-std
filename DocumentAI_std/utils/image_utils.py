# TODO: Gabor, Entropy and every Textural Image
# TODO: Add a library for Embedding (Visaul, Text, and combined)
import torch

from DocumentAI_std.base.doc_element import DocElement


class ImageUtils:
    @staticmethod
    def entropy(doc_element: DocElement) -> float:
        input_tensor = doc_element.extract_pixels()

        # Compute histogram and probabilities
        histogram = torch.histc(input_tensor.float(), bins=int(torch.max(input_tensor)) + 1)
        probabilities = histogram / input_tensor.numel()
        probabilities = probabilities[probabilities != 0]

        # Compute entropy
        epsilon = 1e-10
        return -(probabilities * torch.log2(probabilities + epsilon)).sum().item()


