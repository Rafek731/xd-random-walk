from typing import Any
import numpy as np
from abc import ABC, abstractmethod

class RandomVectorGenerator(ABC):
    """Wrapper class around numpy.random.Generator"""

    __slots__ = ['_dims', '_generator', '_max_step', '_num_samples']
    _dims: int
    """Number of dimensions of the vector"""
    _num_samples: int
    """num random vectors generate"""
    _generator: np.random.Generator
    """Generator for number generation"""
    
    def __init__(self, dims: int, num_samples: int = 1, generator: np.random.Generator|None = None) -> None:
        """Class that generates random vectors of specified length

        Args:
            dims (int): length of the vector
            max_step (float, optional): max number that can appear in vector. Defaults to 1.0.
            generator (np.random.Generator | None, optional): generator used to generate random numbers. Defaults to `np.random.default_rng()`.
        """
        self._dims = dims
        self._num_samples = num_samples
        self._generator = np.random.default_rng() if generator is None else generator

    def generate(self) -> np.ndarray:
        cols = self._generator.integers(0, self._dims, dtype=int)
        vals = self._generate_values()

        random_vectors = np.zeros((self._num_samples, self._dims), dtype=int)
        random_vectors[np.arange(self._num_samples), cols] = vals

        return random_vectors

    def __next__(self) -> np.ndarray:
        return self.generate()

    def __call__(self) -> np.ndarray:
        return self.generate()
    
    @abstractmethod
    def _generate_values(self) -> np.ndarray:
        pass
    
class UniformRVG(RandomVectorGenerator):
    def _generate_values(self) -> np.ndarray:
        return self._generator.uniform(-1,1, self._num_samples)
    
class DiscreteRVG(RandomVectorGenerator):
    def _generate_values(self) -> np.ndarray:
        return self._generator.choice([-1, 1], size=self._num_samples, replace=True)

class NormalRVG(RandomVectorGenerator):
    def _generate_values(self) -> np.ndarray[tuple[Any, ...], np.dtype[Any]]:
        return self._generator.normal(0, 1/3, size=self._num_samples)