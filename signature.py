import os
import hashlib

filename = "./message.txt"
BLOCK_SIZE = 1024

# y^2 = x^3 + ax + b
a = 0
b = 7
inf = 100000000000

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def addPoints(p, q):
    if p.x == q.x and p.y == -q.y:
        r = Point(inf, inf)
    else:
        if p.x == q.x and p.y == q.y:
            k = (3 * pow(p.x, 2) + a) / (2 * p.y)
        else:
            k = (q.y - p.y) / (q.x - p.x)
        x = pow(k, 2) - p.x - q.x
        y = -p.y - k * (x - p.x)
        r = Point(x, y)
    return r

def hashFile(file):
    file_hash = hashlib.sha256()
    with open(file,"r") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb.encode("utf-8"))
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()

print(hashFile(filename))
p = Point(-1.64920,1.58568)
q = Point(2.186988,4.178538)
r = addPoints(p, q)
print(r.x, r.y)


