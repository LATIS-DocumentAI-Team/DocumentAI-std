# TODO: Gabor, Entropy and every Textural Image
# TODO: Add a library for Embedding (Visaul, Text, and combined)
import torch

from DocumentAI_std.base.doc_element import DocElement


class ImageUtils:
    @staticmethod
    def entropy(doc_element: DocElement) -> float:
        """
        Compute the entropy of a document element's pixel values.

        This method calculates the entropy of the pixel values within the bounding box of
        the specified document element.

        Args:
            doc_element (DocElement): The document element containing pixel values.

        Returns:
            float: The entropy value of the pixel values within the document element.

        Note:
            Entropy is a measure of uncertainty or randomness in the pixel values of an image.
            Higher entropy indicates higher disorder or unpredictability in the pixel values.

        Raises:
            ValueError: If the document element does not contain valid pixel values.
        """
        # Extract pixel values from the document element
        input_tensor = doc_element.extract_pixels()

        # Compute histogram and probabilities
        histogram = torch.histc(
            input_tensor.float(), bins=int(torch.max(input_tensor)) + 1
        )
        probabilities = histogram / input_tensor.numel()
        probabilities = probabilities[probabilities != 0]

        # Compute entropy
        epsilon = 1e-10
        entropy = -(probabilities * torch.log2(probabilities + epsilon)).sum().item()

        return entropy
