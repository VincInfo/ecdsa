from random import SystemRandom
import time
from ecdsa import ECDSA, inv, get_y, is_on_curve
        
def pollards_rho(P, Q):
    n = ECDSA.n
    def f(x_i, a_i, b_i):
        if x_i.x == None or x_i.x % 3 == 0:
            return (P + x_i, (a_i + 1) % n, b_i)
        elif x_i.x % 3 == 1:
            return (x_i + x_i, (2 * a_i) % n, (2 * b_i) % n)
        elif x_i.x % 3 == 2:
            return (Q + x_i, a_i, (b_i + 1) % n)

    a_0, b_0 = SystemRandom().randint(1, n-1), SystemRandom().randint(1, n-1)
    x_0 = a_0*P + b_0*Q

    tortoise = x_0, a_0, b_0
    hare = x_0, a_0, b_0

    for i in range(n - 1):
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
        p = k * P
        if p.x == None and p.y == None:
            return k
        k += 1

def find_random_point_between(xs, xe, ys, ye):
    p = (None, None)
    for x in range(xs, xe):
        for y in range(ys, ye):
            if is_on_curve(x, y):
                print('found point')
                p = (x % ECDSA.G.curve.p, y % ECDSA.G.curve.p)
    return p

ps = 10
P = ECDSA.G
print(is_on_curve(P.x, P.y))
n = ECDSA.n
# n = point_order(P)
p = ECDSA.G.curve.p
print(f'order: {n}')

# s = 20000
# x_from = p - s
# y_from = p - s
# x_to = p - s + 10000
# y_to = p - s + 1000
# x, y = find_random_point_between(x_from, x_to, y_from, y_to)
# if x == None or y == None:
#     print('nothing found')
#     exit()
# P = Point(ECDSA.G.curve, x, y)
# print(f'P: ({P.x}, {P.y})')


# print(is_on_curve(P.x, P.y))
# print(is_on_curve(Q.x, Q.y))

def find_k():
    for p in range(ps):
        k = SystemRandom().randint(1, n-1)
        Q = k * P
        print()
        print(f'k: {k}')
        print(f'P: ({P.x}, {P.y})')
        print(f'Q: ({Q.x}, {Q.y}) = [k]P')
        print('searching k...')

        # check = False
        start_time_pollard = time.time()
        while True:
            k_found = pollards_rho(P, Q)
            Q_found = k_found * P 
            # check = Q_found.x == Q.x and Q_found.y == Q.y
            # print(f'control: [{k_found}]P = ({Q_found.x}, {Q_found.y})', end=' ')
            # print(f'== Q ==> correct') if check else print(f'!= Q ==> wrong')
            if Q_found.x == Q.x and Q_found.y == Q.y:
                print(f'pollards rho found: {k_found}')
                break
        end_time_pollard = time.time()

        start_time_brute_force = time.time()
        for i in range(n):
            R = i * P
            if R.x == Q.x and R.y == Q.y:
                print(f'brute force found: {i}')
                break
        end_time_brute_force = time.time()

        time_pollard = end_time_pollard - start_time_pollard
        time_brute_force = end_time_brute_force - start_time_brute_force
        print(f'time - pollards rho: {time_pollard}s')
        print(f'time - brute force: {time_brute_force}s')
            
find_k()

