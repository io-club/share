"""Hash and HMAC algorithms from the standard library of Python."""

import hashlib
import hmac
from abc import ABCMeta
from secrets import token_bytes as random
from typing import Any, Self

from .abc import Digester, Authenticator
from .utils import AlgorithmMapping

__all__ = [
    "HMAC",
]

type _Namespace = dict[str, Any]


class _DigestMetaclass(ABCMeta):
    """Hash digest Metaclass."""

    type __Bases = tuple[type[Digester],]

    def __new__(
        cls, name: str, bases: __Bases, namespace: _Namespace, alg: str
    ) -> "_DigestMetaclass":
        namespace["name"] = alg
        namespace["digest_size"] = hashlib.new(alg).digest_size
        namespace["digest"] = lambda _, data: hashlib.new(alg, data).digest()
        return ABCMeta.__new__(cls, name, bases, namespace)

    def __init__(cls, name: str, bases: __Bases, namespace: _Namespace, _) -> None:
        super().__init__(name, bases, namespace)


digesters = AlgorithmMapping[Digester]()

_hash_cls_names = (
    "MD5",
    "SHA1",
    "SHA224",
    "SHA256",
    "SHA384",
    "SHA512",
    "BLAKE2b",
    "BLAKE2s",
    "SHA3_224",
    "SHA3_256",
    "SHA3_384",
    "SHA3_512",
)
__all__ += _hash_cls_names  # type: ignore
__sha3 = (
    ("sha3-224", "SHA3_224"),
    ("sha3-256", "SHA3_256"),
    ("sha3-384", "SHA3_384"),
    ("sha3-512", "SHA3_512"),
)
for __name in _hash_cls_names:
    __alg = __name.lower()
    exec(
        f"{__name} = {_DigestMetaclass.__name__}('{__name}',"
        f" ({Digester.__name__},), {{}}, '{__alg}')"
    )
    digesters[__alg] = eval(__name)
for __alg, __name in __sha3:
    digesters[__alg] = eval(__name)


class HMAC(Authenticator):
    """HMAC base class."""

    _key: bytes

    def __init__(self, key: bytes) -> None:
        self._key = key

    def to_bytes(self) -> bytes:
        """Dump HMAC to bytes."""
        return self._key

    @classmethod
    def from_bytes(cls, key: bytes) -> Self:
        """Load HMAC from bytes."""
        return cls(key)

    @classmethod
    def generate(cls) -> Self:
        """Generate a new HMAC object."""
        return cls(random(cls.digest_size))


class _HMACMetaclass(ABCMeta):
    """Hash digest Metaclass."""

    type __Bases = tuple[type[HMAC], type[Digester]]

    def __new__(
        cls, name: str, bases: __Bases, namespace: _Namespace, alg: str
    ) -> "_HMACMetaclass":
        namespace["name"] = "hmac-" + alg
        namespace["digest_size"] = hashlib.new(alg).digest_size

        def digest(self: HMAC, data: bytes) -> bytes:
            return hmac.digest(self._key, data, alg)

        namespace["digest"] = digest
        return ABCMeta.__new__(cls, name, bases, namespace)

    def __init__(cls, name: str, bases: __Bases, namespace: _Namespace, _):
        super().__init__(name, bases, namespace)


authenticaters = AlgorithmMapping[Authenticator]()

__HMAC_ALG_HEAD = "hmac"
__HMAC_CLS_HEAD = "HMAC"

_hmac_cls_names = tuple(
    "_".join((__HMAC_CLS_HEAD, __name)) for __name in _hash_cls_names
)

__all__ += _hmac_cls_names  # type: ignore

__alg, __name = None, None

for __name in _hash_cls_names:
    __alg = __name.lower()
    __name = "_".join((__HMAC_CLS_HEAD, __name))
    exec(
        f"{__name} = {_HMACMetaclass.__name__}('{__name}',"
        f" ({HMAC.__name__}, {Digester.__name__}), {{}}, '{__alg}')"
    )
    authenticaters["-".join((__HMAC_ALG_HEAD, __alg))] = eval(__name)
for __alg, __name in __sha3:
    __name = "_".join((__HMAC_CLS_HEAD, __name))
    authenticaters["-".join((__HMAC_ALG_HEAD, __alg))] = eval(__name)

# Cleanup temporary variables
del __alg, __name
