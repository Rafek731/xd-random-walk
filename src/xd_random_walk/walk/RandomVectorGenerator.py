import numpy as np

class RandomVectorGenerator:
    """Wrapper class around numpy.random.Generator"""

    __slots__ = ['_dims', '_generator', '_max_step']
    _dims: int
    """Number of dimensions of the vector"""
    _generator: np.random.Generator
    """Generator for number generation"""
    _max_step: float
    """Max number shown in each of random vector's slot"""
    
    def __init__(self, dims: int, max_step: float = 1.0, generator: np.random.Generator|None = None) -> None:
        """Class that generates random vectors of specified length

        Args:
            dims (int): length of the vector
            max_step (float, optional): max number that can appear in vector. Defaults to 1.0.
            generator (np.random.Generator | None, optional): generator used to generate random numbers. Defaults to `np.random.default_rng()`.

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
        """
        self._dims = dims
        self._generator = np.random.default_rng() if generator is None else generator
        self._max_step = max_step


    def __next__(self):
        return self._generator.uniform(low=0, high=self._max_step, size=self._dims)