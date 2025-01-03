"""resources.lib.passlib.win32 - MS Windows support - DEPRECATED, WILL BE REMOVED IN 1.8

the LMHASH and NTHASH algorithms are used in various windows related contexts,
but generally not in a manner compatible with how passlib is structured.

in particular, they have no identifying marks, both being
32 bytes of binary data. thus, they can't be easily identified
in a context with other hashes, so a CryptHandler hasn't been defined for them.

this module provided two functions to aid in any use-cases which exist.

.. warning::

    these functions should not be used for new code unless an existing
    system requires them, they are both known broken,
    and are beyond insecure on their own.

.. autofunction:: raw_lmhash
.. autofunction:: raw_nthash

See also :mod:`resources.lib.passlib.hash.nthash`.
"""

from warnings import warn
warn("the 'resources.lib.passlib.win32' module is deprecated, and will be removed in "
     "passlib 1.8; please use the 'resources.lib.passlib.hash.nthash' and "
     "'resources.lib.passlib.hash.lmhash' classes instead.",
     DeprecationWarning)

#=============================================================================
# imports
#=============================================================================
# core
from binascii import hexlify
# site
# pkg
from resources.lib.passlib.utils.compat import unicode
from resources.lib.passlib.crypto.des import des_encrypt_block
from resources.lib.passlib.hash import nthash
# local
__all__ = [
    "nthash",
    "raw_lmhash",
    "raw_nthash",
]
#=============================================================================
# helpers
#=============================================================================
LM_MAGIC = b"KGS!@#$%"

raw_nthash = nthash.raw_nthash

def raw_lmhash(secret, encoding="ascii", hex=False):
    """encode password using des-based LMHASH algorithm; returns string of raw bytes, or unicode hex"""
    # NOTE: various references say LMHASH uses the OEM codepage of the host
    #       for its encoding. until a clear reference is found,
    #       as well as a path for getting the encoding,
    #       letting this default to "ascii" to prevent incorrect hashes
    #       from being made w/o user explicitly choosing an encoding.
    if isinstance(secret, unicode):
        secret = secret.encode(encoding)
    ns = secret.upper()[:14] + b"\x00" * (14-len(secret))
    out = des_encrypt_block(ns[:7], LM_MAGIC) + des_encrypt_block(ns[7:], LM_MAGIC)
    return hexlify(out).decode("ascii") if hex else out

#=============================================================================
# eoc
#=============================================================================
