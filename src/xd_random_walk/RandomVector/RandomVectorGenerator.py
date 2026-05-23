from abc import ABC, abstractmethod
from typing import Any

import numpy as np
import numpy.typing as npt


class RandomVectorGenerator(ABC):
    """Abstract base class for generating N-dimensional random vectors.

    This class wraps `numpy.random.Generator` to produce batches of random vectors
    where exactly one randomly selected dimension is modified per step.
    """

    __slots__ = ["_dims", "_num_samples", "_generator", "_data_type"]

    _dims: int
    _num_samples: int
    _generator: np.random.Generator
    _data_type: type | np.dtype

    def __init__(
        self,
        dims: int,
        num_samples: int = 1,
        generator: np.random.Generator | None = None,
    ) -> None:
        """Initializes the random vector generator.

        Args:
            dims (int): The number of dimensions for the generated vectors.
            num_samples (int): The number of independent random vectors to generate per batch.
            generator (np.random.Generator | None, optional): A specific NumPy random generator
                instance. Defaults to `np.random.default_rng()`.
        """
        self._dims = dims
        self._num_samples = num_samples
        self._generator = (
            generator if generator is not None else np.random.default_rng()
        )
        self._data_type = float  # Default type, overridden by concrete subclasses

    def generate(self) -> npt.NDArray[Any]:
        """Generates a batch of random vectors.

        For each sample, exactly one random dimension is chosen to receive a generated value,
        while all other dimensions remain zero.

        Returns:
            npt.NDArray[Any]: A 2D array of shape (num_samples, dims) containing the steps.
        """
        # Choose a random dimension (column) for each sample to modify independently
        cols = self._generator.integers(0, self._dims, size=self._num_samples)
        vals = self._generate_values()

        # Initialize an array of zeros and apply the generated values to the chosen dimensions
        random_vectors = np.zeros(
            (self._num_samples, self._dims), dtype=self._data_type
        )
        random_vectors[np.arange(self._num_samples, dtype=int), cols] = vals

        return random_vectors

    def __next__(self) -> npt.NDArray[Any]:
        """Allows the generator to be used directly as an iterator."""
        return self.generate()

    def __call__(self) -> npt.NDArray[Any]:
        """Allows the generator object to be called as a standard function."""
        return self.generate()

    @abstractmethod
    def _generate_values(self) -> npt.NDArray[Any]:
        """Generates the actual random values to populate the chosen dimensions.

        Returns:
            npt.NDArray[Any]: A 1D array of length `num_samples` containing the random values.
        """
        pass


class DiscreteRVG(RandomVectorGenerator):
    """Generates random vectors with discrete lattice steps of exactly -1 or 1."""

    def __init__(
        self,
        dims: int,
        num_samples: int = 1,
        generator: np.random.Generator | None = None,
    ) -> None:
        super().__init__(dims, num_samples, generator)
        self._data_type = int

    def _generate_values(self) -> npt.NDArray[np.int_]:
        return self._generator.choice([-1, 1], size=self._num_samples, replace=True)


class UniformRVG(RandomVectorGenerator):
    """Generates random vectors with continuous steps uniformly distributed between -1.0 and 1.0."""

    def __init__(
        self,
        dims: int,
        num_samples: int = 1,
        generator: np.random.Generator | None = None,
    ) -> None:
        super().__init__(dims, num_samples, generator)
        self._data_type = float

    def _generate_values(self) -> npt.NDArray[np.float64]:
        return self._generator.uniform(-1.0, 1.0, size=self._num_samples)


class NormalRVG(RandomVectorGenerator):
    """Generates random vectors with continuous steps normally distributed (mean=0, variance=1/3)."""

    def __init__(
        self,
        dims: int,
        num_samples: int = 1,
        generator: np.random.Generator | None = None,
    ) -> None:
        super().__init__(dims, num_samples, generator)
        self._data_type = float

    def _generate_values(self) -> npt.NDArray[np.float64]:
        return self._generator.normal(loc=0.0, scale=1 / 3, size=self._num_samples)
