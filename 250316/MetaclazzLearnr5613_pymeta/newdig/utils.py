""""utils"""

from typing import Self

from .abc import Algorithm

__all__ = [
    "AlgorithmNotFoundError",
    "AlgorithmMapping",
]


class AlgorithmNotFoundError(LookupError, ValueError):
    """Target algorithm not found."""

    __slots__ = ()


class AlgorithmMapping[T: Algorithm](dict[str, type[T]]):
    """Mapping of algorithm classes which raises AlgorithmError instead of KeyError."""

    __slots__ = ()

    @classmethod
    def from_algorithms(cls, *algs: type[T]) -> Self:
        """Return a instance from algorithm classes."""
        return cls({alg.name: alg for alg in algs})

    def __getitem__(self, *args, **kwargs):
        try:
            return super().__getitem__(*args, **kwargs)
        except KeyError as err:
            raise AlgorithmNotFoundError from err
