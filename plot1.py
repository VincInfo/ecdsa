from matplotlib import pyplot as plt
from ecdsa import ECDSA


def successive_points(k):
    points = []
    point = ECDSA.G
    for _ in range(k):
        points.append(point)
        point = point + ECDSA.G
    return points


k = 60
P = successive_points(k)

plt.figure()

plt.scatter(P[0].x, P[0].y, label="dots", color="red", marker="x", s=20)
plt.text(P[0].x, P[0].y, "G", fontsize=15, ha="left", va="bottom")

for p in P[1:]:
    if p is not None:
        print(p.x, p.y)
        plt.scatter(p.x, p.y, label="dots", color="black", marker="x", s=20)

plt.scatter(P[-1].x, P[-1].y, label="dots", color="red", marker="x", s=20)
plt.text(P[-1].x, P[-1].y, f"[{k}]G", fontsize=15, ha="left", va="bottom")

plt.xlabel("x")
plt.ylabel("y")
plt.show()
