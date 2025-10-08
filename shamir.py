import random

_PRIME = 2**61 - 1 

def mod_inverse(k, p):
    return pow(k % p, -1, p)

def create_shares(secret, n, t, p=_PRIME):
    """
    Make n shares with threshold t for 'secret'.
    Polynomial: f(x) = a0 + a1 x + ... + a_{t-1} x^{t-1}, where a0 = secret.
    """
    secret %= p
    # a0 = secret; a1..a_{t-1} = random
    coeffs = [secret] + [random.randrange(p) for _ in range(t - 1)]

    shares = []
    for x in range(1, n + 1):
        y = 0
        for a in reversed(coeffs):
            y = (y * x + a) % p # horner's method
        shares.append((x, y))
    return shares

def reconstruct_secret(shares, p=_PRIME):
    """
    This one is used to reconstruct the secret from given shares.
    """
    x_coords, y_coords = zip(*shares) # x: coordinates, y: f(x) values
    secret = 0
    for i in range(len(shares)): # loop over each share
        xi, yi = x_coords[i], y_coords[i]
        num, den = 1, 1
        for j in range(len(shares)):
            if i == j: 
                continue # skip its own share
            xj = x_coords[j]
            num = (num * (-xj % p)) % p         
            den = (den * ((xi - xj) % p)) % p   
        li0 = (num * mod_inverse(den, p)) % p  
        secret = (secret + yi * li0) % p
    return secret

def shamir_avg(values, p=_PRIME):
    """
    Secure-sum via Shamir, then divide in the clear to get the (float) average.
    """
    n = len(values)
    if n == 0:
        return 0.0
    t = n // 2 + 1 # threshold

    # Phase 1
    all_received = [[] for i in range(n)]
    for v in values:
        shares = create_shares(v, n, t, p)
        for i in range(n):
            all_received[i].append(shares[i])

    # Phase 2
    summed_shares = []
    for i in range(n):
        y_sum = sum(y for _, y in all_received[i]) % p
        summed_shares.append((i + 1, y_sum))  # keep same x

    # Phase 3
    total_sum = reconstruct_secret(summed_shares[:t], p)
    return total_sum / n
