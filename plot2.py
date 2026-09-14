import numpy as np
import matplotlib.pyplot as plt
from ecdsa import ECDSA


def successive_points(k):
    points = []
    point = ECDSA.G
    for _ in range(k):
        points.append(point)
        point = point + ECDSA.G
    return points


p = ECDSA.G.curve.p
k = 60
P = successive_points(k)
s = len(P)


def torus(u, v, R, r):
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    return x, y, z


R = p / (np.pi * 2)
r = R / 2
u = np.linspace(0, 2 * np.pi, 200)
v = np.linspace(0, 2 * np.pi, 200)
U, V = np.meshgrid(u, v)
X, Y, Z = torus(U, V, R, r)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_zlim(-R, R)
ax.plot_surface(X, Y, Z, rstride=5, cstride=5, color="gray", alpha=0.5)
ax.view_init(36, 26)

mapping = (2 * np.pi) / p
for point in P[1 : s - 2]:
    u = point.x * mapping
    v = point.y * mapping
    x, y, z = torus(u, v, R, r)
    ax.scatter(x, y, z, color="black", s=10)

x1, y1, z1 = torus(P[0].x * mapping, P[0].y * mapping, R, r)
ax.scatter(x1, y1, z1, color="red", s=20)
ax.text(x1, y1, z1, "G", fontsize=15, ha="left", va="bottom")

x2, y2, z2 = torus(P[-1].x * mapping, P[-1].y * mapping, R, r)
ax.scatter(x2, y2, z2, color="red", s=20)
ax.text(x2, y2, z2, f"[{k}]G", fontsize=15, ha="left", va="bottom")

plt.show()
