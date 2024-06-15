from random import SystemRandom
import time
from ecdsa import ECDSA, Point, inv, get_y, is_on_curve
from sympy.ntheory import factorint
        
def pollards_rho(P, Q):
    # n = 673
    # n = point_order(P)
    n = ECDSA.n
    def f(x_i, a_i, b_i):
        if x_i.x == None or x_i.x % 3 == 0:
            return (P + x_i, (a_i + 1) % n, b_i)
        elif x_i.x % 3 == 1:
            return (x_i + x_i, (2 * a_i) % n, (2 * b_i) % n)
        elif x_i.x % 3 == 2:
            return (Q + x_i, a_i, (b_i + 1) % n)

    a_0, b_0 = SystemRandom().randint(1, n-1), SystemRandom().randint(1, n-1)
    # print(f'retrying with {a_0}, {b_0}')
    x_0 = a_0*P + b_0*Q

    tortoise = x_0, a_0, b_0
    hare = x_0, a_0, b_0

    for i in range(n - 1):
        # print(f'i: {i}')
        tortoise = f(*tortoise)
        hare = f(*f(*hare))
        x_i_t, a_i_t, b_i_t = tortoise
        x_i_h, a_i_h, b_i_h = hare
        if x_i_t.x == x_i_h.x and x_i_t.y == x_i_h.y:
            if b_i_h != b_i_t:
                a = (a_i_h - a_i_t) % n 
                b = inv(b_i_t - b_i_h, n) % n 
                k = (a * b) % n
                return k
            else:
                print('invalid collision')
    print(f'nothing found')

def find_point_on_curve():
    x = 1
    while True:
        y = get_y(x)
        if(isinstance(y, int)):
            return (x, y)
        x += 1

def point_order(P):
    k = 1
    while True:
        # print(f'k: {k}')
        p = k * P
        if p.x == None and p.y == None:
            return k
        k += 1

def find_random_point_between(xs, xe, ys, ye):
    p = (None, None)
    for x in range(xs, xe):
        for y in range(ys, ye):
            # print(x, y)
            if is_on_curve(x, y):
                print('found point')
                p = (x % ECDSA.G.curve.p, y % ECDSA.G.curve.p)
                # return p
    return p

ps = 100
P = ECDSA.G
print(is_on_curve(P.x, P.y))
# n = point_order(P)
n = ECDSA.n
p = ECDSA.G.curve.p
# print(f'order: {n}')

# s = 200000
# x_from = p - s
# y_from = p - s
# x_to = p - s + 10000
# y_to = p - s + 1000
# x, y = find_random_point_between(x_from, x_to, y_from, y_to)
# if x == None or y == None:
#     print('nothing found')
#     exit()
# P = Point(ECDSA.G.curve, x, y)
# Q = k * P

# print(f'k: {k}')
# print(f'P: ({P.x}, {P.y})')
# print(f'Q: ({Q.x}, {Q.y}) = [k]P')

# print(is_on_curve(P.x, P.y))
# print(is_on_curve(Q.x, Q.y))

for p in range(ps):
    k = SystemRandom().randint(1, n-1)
    Q = k * P
    # print(f'P: ({P.x}, {P.y})')

    # print(is_on_curve(P.x, P.y))

    # print(is_on_curve(2, 63))
    # print(get_y(2))

    print(f'k: {k}')
    print(f'P: ({P.x}, {P.y})')
    print(f'Q: ({Q.x}, {Q.y}) = [k]P')

    # o = point_order(P)
    print(f'order: {n}')
    point = n * P
    print(f'[{n}]P = ({point.x}, {point.y})')

    print('searching k...')
    print()
    check = False
    start_time_pollard = time.time()
    while not check:
        k_found = pollards_rho(P, Q)
        # print(f'k found: k = {k_found}')
        Q_found = k_found * P 
        check = Q_found.x == Q.x and Q_found.y == Q.y
        # print(f'control: [{k_found}]P = ({Q_found.x}, {Q_found.y})', end=' ')
        # print(f'== Q ==> correct') if check else print(f'!= Q ==> wrong')
        if check:
            print(f'found: {k_found}')
            break
        # else:
        #     print('retrying')
    end_time_pollard = time.time()

    start_time_brute_force = time.time()
    for i in range(n):
        R = i * P
        if R.x == Q.x and R.y == Q.y:
            print(f'found: {i}')
            break
    end_time_brute_force = time.time()

    time_pollard = end_time_pollard - start_time_pollard
    time_brute_force = end_time_brute_force - start_time_brute_force
    print(f'pollards rho: {time_pollard}')
    print(f'brute force: {time_brute_force}')
        


