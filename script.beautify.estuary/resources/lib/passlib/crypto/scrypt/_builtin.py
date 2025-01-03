"""resources.lib.passlib.utils.scrypt._builtin -- scrypt() kdf in pure-python"""
#==========================================================================
# imports
#==========================================================================
# core
import operator
import struct
# pkg
from resources.lib.passlib.utils.compat import izip
from resources.lib.passlib.crypto.digest import pbkdf2_hmac
from resources.lib.passlib.crypto.scrypt._salsa import salsa20
# local
__all__ =[
    "ScryptEngine",
]

#==========================================================================
# scrypt engine
#==========================================================================
class ScryptEngine(object):
    """
    helper class used to run scrypt kdf, see scrypt() for frontend

    .. warning::
        this class does NO validation of the input ranges or types.

        it's not intended to be used directly,
        but only as a backend for :func:`resources.lib.passlib.utils.scrypt.scrypt()`.
    """
    #=================================================================
    # instance attrs
    #=================================================================

    # primary scrypt config parameters
    n = 0
    r = 0
    p = 0

    # derived values & objects
    smix_bytes = 0
    iv_bytes = 0
    bmix_len = 0
    bmix_half_len = 0
    bmix_struct = None
    integerify = None

    #=================================================================
    # frontend
    #=================================================================
    @classmethod
    def execute(cls, secret, salt, n, r, p, keylen):
        """create engine & run scrypt() hash calculation"""
        return cls(n, r, p).run(secret, salt, keylen)

    #=================================================================
    # init
    #=================================================================
    def __init__(self, n, r, p):
        # store config
        self.n = n
        self.r = r
        self.p = p
        self.smix_bytes = r << 7  # num bytes in smix input - 2*r*16*4
        self.iv_bytes = self.smix_bytes * p
        self.bmix_len = bmix_len = r << 5  # length of bmix block list - 32*r integers
        self.bmix_half_len = r << 4
        assert struct.calcsize("I") == 4
        self.bmix_struct = struct.Struct("<" + str(bmix_len) + "I")

        # use optimized bmix for certain cases
        if r == 1:
            self.bmix = self._bmix_1

        # pick best integerify function - integerify(bmix_block) should
        # take last 64 bytes of block and return a little-endian integer.
        # since it's immediately converted % n, we only have to extract
        # the first 32 bytes if n < 2**32 - which due to the current
        # internal representation, is already unpacked as a 32-bit int.
        if n <= 0xFFFFffff:
            integerify = operator.itemgetter(-16)
        else:
            assert n <= 0xFFFFffffFFFFffff
            ig1 = operator.itemgetter(-16)
            ig2 = operator.itemgetter(-17)
            def integerify(X):
                return ig1(X) | (ig2(X)<<32)
        self.integerify = integerify

    #=================================================================
    # frontend
    #=================================================================
    def run(self, secret, salt, keylen):
        """
        run scrypt kdf for specified secret, salt, and keylen

        .. note::

            * time cost is ``O(n * r * p)``
            * mem cost is ``O(n * r)``
        """
        # stretch salt into initial byte array via pbkdf2
        iv_bytes = self.iv_bytes
        input = pbkdf2_hmac("sha256", secret, salt, rounds=1, keylen=iv_bytes)

        # split initial byte array into 'p' mflen-sized chunks,
        # and run each chunk through smix() to generate output chunk.
        smix = self.smix
        if self.p == 1:
            output = smix(input)
        else:
            # XXX: *could* use threading here, if really high p values encountered,
            #      but would tradeoff for more memory usage.
            smix_bytes = self.smix_bytes
            output = b''.join(
                smix(input[offset:offset+smix_bytes])
                for offset in range(0, iv_bytes, smix_bytes)
            )

        # stretch final byte array into output via pbkdf2
        return pbkdf2_hmac("sha256", secret, output, rounds=1, keylen=keylen)

    #=================================================================
    # smix() helper
    #=================================================================
    def smix(self, input):
        """run SCrypt smix function on a single input block

        :arg input:
            byte string containing input data.
            interpreted as 32*r little endian 4 byte integers.

        :returns:
            byte string containing output data
            derived by mixing input using n & r parameters.

        .. note:: time & mem cost are both ``O(n * r)``
        """
        # gather locals
        bmix = self.bmix
        bmix_struct = self.bmix_struct
        integerify = self.integerify
        n = self.n

        # parse input into 32*r integers ('X' in scrypt source)
        # mem cost -- O(r)
        buffer = list(bmix_struct.unpack(input))

        # starting with initial buffer contents, derive V s.t.
        # V[0]=initial_buffer ... V[i] = bmix(V[i-1], V[i-1]) ... V[n-1] = bmix(V[n-2], V[n-2])
        # final buffer contents should equal bmix(V[n-1], V[n-1])
        #
        # time cost -- O(n * r) -- n loops, bmix is O(r)
        # mem cost -- O(n * r) -- V is n-element array of r-element tuples
        # NOTE: could do time / memory tradeoff to shrink size of V
        def vgen():
            i = 0
            while i < n:
                last = tuple(buffer)
                yield last
                bmix(last, buffer)
                i += 1
        V = list(vgen())

        # generate result from X & V.
        #
        # time cost -- O(n * r) -- loops n times, calls bmix() which has O(r) time cost
        # mem cost -- O(1) -- allocates nothing, calls bmix() which has O(1) mem cost
        get_v_elem = V.__getitem__
        n_mask = n - 1
        i = 0
        while i < n:
            j = integerify(buffer) & n_mask
            result = tuple(a ^ b for a, b in izip(buffer, get_v_elem(j)))
            bmix(result, buffer)
            i += 1

        # # NOTE: we could easily support arbitrary values of ``n``, not just powers of 2,
        # #       but very few implementations have that ability, so not enabling it for now...
        # if not n_is_log_2:
        # while i < n:
        #     j = integerify(buffer) % n
        #     tmp = tuple(a^b for a,b in izip(buffer, get_v_elem(j)))
        #     bmix(tmp,buffer)
        #     i += 1

        # repack tmp
        return bmix_struct.pack(*buffer)

    #=================================================================
    # bmix() helper
    #=================================================================
    def bmix(self, source, target):
        """
        block mixing function used by smix()
        uses salsa20/8 core to mix block contents.

        :arg source:
            source to read from.
            should be list of 32*r 4-byte integers
            (2*r salsa20 blocks).

        :arg target:
            target to write to.
            should be list with same size as source.
            the existing value of this buffer is ignored.

        .. warning::

            this operates *in place* on target,
            so source & target should NOT be same list.

        .. note::

            * time cost is ``O(r)`` -- loops 16*r times, salsa20() has ``O(1)`` cost.

            * memory cost is ``O(1)`` -- salsa20() uses 16 x uint4,
              all other operations done in-place.
        """
        ## assert source is not target
        # Y[-1] = B[2r-1], Y[i] = hash( Y[i-1] xor B[i])
        # B' <-- (Y_0, Y_2 ... Y_{2r-2}, Y_1, Y_3 ... Y_{2r-1}) */
        half = self.bmix_half_len # 16*r out of 32*r - start of Y_1
        tmp = source[-16:] # 'X' in scrypt source
        siter = iter(source)
        j = 0
        while j < half:
            jn = j+16
            target[j:jn] = tmp = salsa20(a ^ b for a, b in izip(tmp, siter))
            target[half+j:half+jn] = tmp = salsa20(a ^ b for a, b in izip(tmp, siter))
            j = jn

    def _bmix_1(self, source, target):
        """special bmix() method optimized for ``r=1`` case"""
        B = source[16:]
        target[:16] = tmp = salsa20(a ^ b for a, b in izip(B, iter(source)))
        target[16:] = salsa20(a ^ b for a, b in izip(tmp, B))

    #=================================================================
    # eoc
    #=================================================================

#==========================================================================
# eof
#==========================================================================
