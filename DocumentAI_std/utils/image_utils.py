# TODO: Gabor, Entropy and every Textural Image
# TODO: Add a library for Embedding (Visaul, Text, and combined)
import torch
from scipy import ndimage

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

    @staticmethod
    def gabor_feature(
        doc_element: DocElement, frequency: float, theta: float, sigma: float
    ) -> torch.Tensor:
        """
        Compute the Gabor feature of a document element.

        This method calculates the Gabor feature of the pixel values within the bounding box of
        the specified document element.

        Args:
            doc_element (DocElement): The document element containing pixel values.
            frequency (float): The frequency of the Gabor filter.
            theta (float): The orientation of the Gabor filter (in radians).
            sigma (float): The standard deviation of the Gaussian envelope.

        Returns:
            torch.Tensor: The Gabor feature map of the pixel values within the document element.

        Raises:
            ValueError: If the document element does not contain valid pixel values.
        """
        # Extract pixel values from the document element
        input_tensor = doc_element.extract_pixels()

        # Convert input tensor to numpy array
        input_array = input_tensor.numpy()

        # Apply Gabor filter
        gabor_filter = ndimage.gaussian_filter(input_array, sigma)
        gabor_feature = ndimage.gabor_filter(gabor_filter, frequency, theta)

        # Convert output to torch tensor
        gabor_feature_tensor = torch.tensor(gabor_feature)

        return gabor_feature_tensor
