import hashlib
from random import SystemRandom

__all__ = ['ECDSA']

BLOCK_SIZE = 1024

class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

class Curve: 
    """elliptic curve of the form y^2 = x^3 + a*x + b"""
    def __init__(self, p, a, b):
        self.p = p      # elliptic Curve exists over the field of integers modulo this prime
        self.a = a      # the curve parameter a
        self.b = b      # the curve parameter b

class Point:
    def __init__(self, curve: Curve, x, y):
        self.curve = curve
        self.x = x
        self.y = y

    def __add__(self, other):
        """group operation of elliptic curves"""
        if self == INF:
            return other
        if other == INF:
            return self
        if self.x == other.x and self.y != other.y:
            return INF
        elif self.x == other.x:
            k = (3 * self.x**2 + self.curve.a) * inv(2 * self.y, self.curve.p)
        else:
            k = (self.y - other.y) * inv(self.x - other.x, self.curve.p)
        x = (k**2 - self.x - other.x) % self.curve.p
        y = (-(k*(x - self.x) + self.y)) % self.curve.p
        return Point(self.curve, x, y)
    
    def __rmul__(self, k):
        """calls the group operation the number of k's bits times"""
        result = INF
        append = self
        while k:
            if k & 1:
                result += append
            append += append
            k >>= 1
        return result
    
class Generator:
    def __init__(self, G, n):
        self.G = G
        self.n = n

def hash(file):
    file_hash = hashlib.sha256()
    with open(file,"r") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb.encode("utf-8"))
            fb = f.read(BLOCK_SIZE)
    return int.from_bytes(bytes.fromhex(file_hash.hexdigest()), byteorder='big')

def inv(n, p):
    old_r, r = n, p
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_s % p

def sign(private_key, m):

    z = hash(m)

    k = SystemRandom().randint(1, ECDSA.n-1)
    P = k * ECDSA.G

    r = P.x 
    s = inv(k, ECDSA.n) * (z + private_key * r) % ECDSA.n
    if s > ECDSA.n / 2:
        s = ECDSA.n - s
    return Signature(r, s)

def verify(public_key: Point, m: str, sig: Signature):
    z = hash(m)

    w = inv(sig.s, ECDSA.n)

    u1 = z * w % ECDSA.n
    u2 = sig.r * w % ECDSA.n
    P = (u1 * ECDSA.G) + (u2 * public_key)
    match = P.x == sig.r
    return match

def is_on_curve(x, y, p): 
    return (y**2) % p == (x**3 + 7) % p

def setup():
    a = 0x0000000000000000000000000000000000000000000000000000000000000000 
    b = 0x0000000000000000000000000000000000000000000000000000000000000007
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    #n = 2**256 - 2**224 + 2**192 + 2**96 - 1  
    # secp256k1                                                                                                         
    curve = Curve(p, a, b)
    G = Point(curve, Gx, Gy)
    return Generator(G, n)

ECDSA = setup()

INF = Point(None, None, None)

# m = "./message.txt" 

# private_key = SystemRandom().randint(1, ECDSA.n-1)
# public_key = private_key * ECDSA.G

# sig = sign(private_key, m)

# verify = verify(public_key, m, sig)
# print(verify)

