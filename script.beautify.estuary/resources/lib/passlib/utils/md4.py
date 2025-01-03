"""
resources.lib.passlib.utils.md4 - DEPRECATED MODULE, WILL BE REMOVED IN 2.0

MD4 should now be looked up through ``resources.lib.passlib.crypto.digest.lookup_hash("md4").const``,
which provides unified handling stdlib implementation (if present).
"""
#=============================================================================
# issue deprecation warning for module
#=============================================================================
from warnings import warn
warn("the module 'resources.lib.passlib.utils.md4' is deprecated as of Passlib 1.7, "
     "and will be removed in Passlib 2.0, please use "
     "'lookup_hash(\"md4\").const()' from 'resources.lib.passlib.crypto' instead",
     DeprecationWarning)

#=============================================================================
# backwards compat exports
#=============================================================================
__all__ = ["md4"]

# this should use hashlib version if available,
# and fall back to builtin version.
from resources.lib.passlib.crypto.digest import lookup_hash
md4 = lookup_hash("md4").const
del lookup_hash

#=============================================================================
# eof
#=============================================================================
