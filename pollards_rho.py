from ecdsa import ECDSA, inv
        
def pollards_rho(P, Q):
    n = 673
    def f(x_i, a_i, b_i):
        if x_i.x == None or x_i.x % 3 == 0:
            return (P + x_i, (a_i + 1) % n, b_i)
        elif x_i.x % 3 == 1:
            return (x_i + x_i, (2 * a_i) % n, (2 * b_i) % n)
        elif x_i.x % 3 == 2:
            return (Q + x_i, a_i, (b_i + 1) % n)

    a_0, b_0 = 1, 0
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

k = 363
P = ECDSA.G
Q = k * P

print(f'k: {k}')
print(f'P: ({P.x}, {P.y})')
print(f'Q: ({Q.x}, {Q.y}) = [k]P')

print('searching k...')
print()
k_found = pollards_rho(P, Q)
print(f'k found: k = {k_found}')
Q_found = k_found * P 
check = Q_found.x == Q.x and Q_found.y == Q.y
print(f'control: [{k_found}]P = ({Q_found.x}, {Q_found.y})', end=' ')
print(f'== Q ==> correct') if check else print(f'!= Q ==> wrong')

