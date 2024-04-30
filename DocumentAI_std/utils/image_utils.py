# TODO: Add a library for Embedding (Visaul, Text, and combined)
import math

import torch
from skimage.filters import gabor

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
    def gabor_blank_filter(doc_element, scales, orientations):
        """
        Generates a custom Gabor filter.

        Parameters:
            doc_element (DocElement): The document element containing pixel values.
            scales (int): Number of scales (frequencies).
            orientations (int): Number of orientations.

        Returns:
            torch.Tensor: A tensor with shape = (scales, orientations, doc_element.h, doc_element.w).
        """
        fmax = 0.25
        gamma = math.sqrt(2)
        eta = math.sqrt(2)
        input_tensor = doc_element.extract_pixels()
        output = torch.empty(
            (scales, orientations, doc_element.h, doc_element.w), dtype=torch.float32
        )

        for i in range(scales):
            fi = fmax / (math.sqrt(2) ** i)
            alpha = fi / gamma
            beta = fi / eta
            for j in range(orientations):
                theta = math.pi * (j / orientations)
                filt_real, filt_imag = gabor(
                    input_tensor, fi, theta, sigma_x=alpha, sigma_y=beta
                )
                gabor_out = torch.abs(filt_real + 1j * filt_imag)
                output[i, j] = gabor_out

        return output

    @staticmethod
    def gabor_feature(doc_element, scales, orientations, d1, d2):
        """
        Extracts the Gabor features of an input image.

        Parameters:
            doc_element (DocElement): The document element containing pixel values.
            scales (int): Number of scales (frequencies).
            orientations (int): Number of orientations.
            d1 (int): The factor of downsampling along rows.
            d2 (int): The factor of downsampling along columns.

        Returns:
            torch.Tensor: A tensor with shape = (doc_element.h // d1, doc_element.w // d2, (scales * orientations) / (d1 * d2)).
        """
        gabor_abs = ImageUtils.gabor_blank_filter(doc_element, scales=3, orientations=6)
        feature_list = []

        for i in range(scales):
            for j in range(orientations):
                feature_list.append(gabor_abs[i, j, ::d1, ::d2].view(-1))

        output = torch.cat(feature_list).view(
            doc_element.h // d1, doc_element.w // d2, scales * orientations
        )
        return output

    @staticmethod
    def gabor_decomposition(doc_element, scales, orientations, d1=1, d2=1):
        """
        Obtains the Gabor feature vector of an input image.

        Parameters:
            doc_element (DocElement): The document element containing pixel values.
            scales (int): Number of scales (frequencies).
            orientations (int): Number of orientations.
            d1 (int): The factor of downsampling along rows.
            d2 (int): The factor of downsampling along columns.

        Returns:
            torch.Tensor: A tensor with shape = (doc_element.h // d1, doc_element.w // d2, (scales * orientations) / (d1 * d2)).
        """
        feat_v = ImageUtils.gabor_feature(doc_element, scales, orientations, d1, d2)

        max_feat = feat_v.max(dim=2, keepdim=True)[0]
        max_feat[max_feat == 0.0] = 1.0
        feat_v = feat_v / max_feat
        feat_v = torch.clamp(feat_v, min=0.0, max=0.5) * 512

        return feat_v
