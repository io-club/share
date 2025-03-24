"""Simple no crypto implement."""

from collections.abc import Callable
from secrets import token_bytes as random
from typing import Self

from .abc import (
    ConstructibleAlgorithm,
    Digester,
    Authenticator,
)
from .utils import AlgorithmMapping

__all__ = (
    "NoDigest",
    "NoMac",
)


class NoDigest(Digester):
    """Digest into nothing."""

    name = "none"
    digest_size = 0

    def digest(self, _: bytes) -> bytes:
        """Return empty bytes."""
        return b""


digests = AlgorithmMapping[Digester].from_algorithms(NoDigest)


class NoMAC(Authenticator, NoDigest):
    """No MAC."""

    def digest(self, _: bytes) -> bytes:
        """Return empty bytes."""
        return b""

    def to_bytes(self) -> bytes:
        """Return empty bytes."""
        return b""

    @classmethod
    def from_bytes(cls, _: bytes) -> Self:
        """Return an instance."""
        return cls()

    @classmethod
    def generate(cls) -> Self:
        """Return an instance."""
        return cls()


authenticators = AlgorithmMapping[Authenticator].from_algorithms(NoMAC)
