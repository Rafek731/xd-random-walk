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
    _max_step: float
    """Max number shown in each of random vector's slot"""
    
    def __init__(self, dims: int, num_samples: int = 1,  max_step: float = 1.0, generator: np.random.Generator|None = None) -> None:
        """Class that generates random vectors of specified length

        Args:
            dims (int): length of the vector
            max_step (float, optional): max number that can appear in vector. Defaults to 1.0.
            generator (np.random.Generator | None, optional): generator used to generate random numbers. Defaults to `np.random.default_rng()`.
        """
        self._dims = dims
        self._num_samples = num_samples
        self._generator = np.random.default_rng() if generator is None else generator
        self._max_step = max_step

    @abstractmethod
    def __next__(self) -> np.ndarray:
        pass

    @abstractmethod
    def __call__(self) -> np.ndarray:
        pass
        
    
class UniformRVG(RandomVectorGenerator):
    def step(self) -> np.ndarray:
        return self._generator.uniform(low=-self._max_step, high=self._max_step, size=(self._num_samples, self._dims))
    def __next__(self) -> np.ndarray:
        return self.step()
    
    def __call__(self) -> np.ndarray:
        return self.step()
    
class DiscreteRVG(RandomVectorGenerator):
    def __next__(self) -> np.ndarray:
        return self._generator.choice([-1,1], size=(self._num_samples, self._dims), replace=True)
    
    def __call__(self) -> np.ndarray:
        return self._generator.choice([-1,1], size=(self._num_samples, self._dims), replace=True)