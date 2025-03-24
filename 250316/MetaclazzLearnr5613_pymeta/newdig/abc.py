""" "Hi."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Self

__all__ = [
    "Algorithm",
    "SerializableAlgorithm",
    "ConstructibleAlgorithm",
    "Digester",
    "Authenticator",
]

class Algorithm(ABC):
    """Algorithm with name."""

    __slots__ = ()

    name: str

    def __repr__(self) -> str:
        return f"{self.name} object at {hex(id(self))}>"


class SerializableAlgorithm(Algorithm):
    """Algorithm base class with self.to_bytes() -> bytes."""

    __slots__ = ()

    @abstractmethod
    def to_bytes(self) -> bytes:
        """Dump instance to bytes."""

    def __eq__(self, other: object, /) -> bool:
        return self is other or (
            isinstance(other, SerializableAlgorithm)
            and self.name == other.name
            and self.to_bytes() == other.to_bytes()
        )

    def __str__(self) -> str:
        return self.to_bytes().hex()

    def __repr__(self) -> str:
        return f"<{self.name}: {str(self)}>"


class ConstructibleAlgorithm(SerializableAlgorithm):
    """Algorithm base class with cls.from_bytes(data: bytes) -> Self."""

    __slots__ = ()

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes, /) -> Self:
        """Load instance from bytes."""

    def __copy__(self) -> Self:
        return type(self).from_bytes(self.to_bytes())


class Digester(Algorithm):
    """Message digester base class.

    Example

    >>> from newdig import digesters
    >>> dig = digesters['md5']()
    >>> msg = b'message'
    >>> dig.digest(msg).hex()
    '78e731027d8fd50ed642340b7c9a63b3'

    """

    __slots__ = ()

    digest_size: int

    @abstractmethod
    def digest(self, data: bytes, /) -> bytes:
        """Return the digest of the data."""


class Authenticator(ConstructibleAlgorithm, Digester):
    """Message authenticater of MAC algorithm base class.

    Example

    >>> from newdig import authenticators
    >>> msg = b'message'
    >>> key = b'the secret bytes'
    >>> aut = authenticators['hmac-md5'].from_bytes(key)
    >>> aut.digest(msg).hex()
    '45b958e68d026ebb4d5ad210d819aed7'

    """

    __slots__ = ()

    @classmethod
    @abstractmethod
    def generate(cls) -> Self:
        """Generate a MAC instance."""


if __name__ == "__main__":
    import doctest

    doctest.testmod()
