import numpy as np
from typing import Any, Iterable, List, Tuple


class ZipFeaturizer(object):
    def __init__(self, n_bins: int = 512) -> "ZipFeaturizer":
        self.n_bins = n_bins

    def __call__(self, smiles: Iterable[str]) -> Tuple[np.ndarray, List[int]]:
        return self.featurize(smiles)

    def bin_vectors(self, X: Iterable[str]):
        """
        Convert a 2D numpy array of vectors into a list of string representations based on binning.

        Parameters:
        - X (numpy.ndarray): A 2D array of shape (n_samples, n_features) to be binned.
        - num_bins (int): The number of bins to be used for binning.

        Returns:
        - list: A list of string representations of the binned vectors.

        Description:
        The function first determines the global minimum and maximum values across all vectors.
        It then creates separate bins for positive and negative values. Each value in the vectors
        is then assigned to a bin and represented by a unique Unicode character. Negative values
        are prefixed with a special '✖' character. The binned representations of the vectors are
        then returned as a list of strings.
        """

        # Create bins for positive and negative numbers separately
        X_flattened = X.flatten()
        pos_vector = X_flattened[X_flattened >= 0]
        neg_vector = -X_flattened[X_flattened < 0]  # Flip sign for binning

        pos_bins = np.linspace(
            0, max(pos_vector) if len(pos_vector) > 0 else 1, self.n_bins + 1
        )
        neg_bins = np.linspace(
            0, max(neg_vector) if len(neg_vector) > 0 else 1, self.n_bins + 1
        )

        # Create a mapping from bin number to Unicode character
        bin_to_char = {i + 1: chr(9786 + i) for i in range(self.n_bins)}

        # Apply binning to each vector
        string_reps = []
        for vector in X:
            # Digitize the vectors
            pos_digitized = np.digitize(vector[vector >= 0], pos_bins)
            neg_digitized = np.digitize(-vector[vector < 0], neg_bins)

            # Convert digitized vectors to string representation
            pos_string_rep = [bin_to_char.get(num, "?") for num in pos_digitized]
            neg_string_rep = [f'✖{bin_to_char.get(num, "?")}' for num in neg_digitized]

            # Combine the representations in the original order
            string_rep = []
            pos_index = 0
            neg_index = 0
            for num in vector:
                if num >= 0:
                    string_rep.append(pos_string_rep[pos_index])
                    pos_index += 1
                else:
                    string_rep.append(neg_string_rep[neg_index])
                    neg_index += 1

            string_reps.append("".join(string_rep))

        return string_reps