"""Provide crypto SPI and basic crypto algorithms."""

__version__ = "1.-1.0"

from .abc import (
    Digester,
    Authenticator,
)
from .utils import AlgorithmMapping

from . import (
    none,
    stdauth,
)

__all__ = [
    "abc",
    "utils",
    "digesters",
    "authenticators",
    "none",
    "stdauth",
]

# Crypto collections
digesters = AlgorithmMapping[Digester]()
authenticators = AlgorithmMapping[Authenticator]()

digesters |= none.digests
authenticators |= none.authenticators

digesters |= stdauth.digesters
authenticators |= stdauth.authenticaters
