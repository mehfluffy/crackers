from functools import reduce
from numpy import lcm, gcd, floor

def factorize(n):    
    factors = list(
        reduce(
            list.__add__,
            ([i, n // i] for i in range(1, int(n**0.5) + 1) if n % i == 0)
        )
    )
    return factors

def gcd_euclid_ext(a, b):  # doesn't work to find the inverse
    '''a*x + b*y = gcd(a, b)'''
    if a == 0:
        return 0, 1, b
    x1, y1, gcd = gcd_euclid_ext(b%a, a)
    x = y1 - (b // a) * x1
    y = x1
    return x, y, gcd


def use_rsa():
    # choose p and q:
    p = int(input("Enter prime 1: "))
    q = int(input("Enter prime 2, different from prime 1: "))
    n = p * q

    # compute phi, lambda:
    phi = (p - 1) * (q - 1)
    lam = lcm(p - 1, q - 1)

    # choose e:
    e_choices = []
    for i in range(1, lam):
        if phi % i != 0 and len(factorize(i)) == 2:
            e_choices.append(i)
    if len(e_choices) > 1:
        e = int(input(f"Choose e as one of {e_choices}:"))
    elif len(e_choices) == 1:
        e = e_choices[0]
        print("Only 1 choice for e found, using:", e)
    else:
        print("No choices for e found, please choose bigger primes for p and q.")
        return

    # compute d:
    #d = e ** (phi - 1) % phi   # this works, but isn't correct
    k = 1
    while k > 0:
        d = (1 + k*phi) / e
        if floor(d) == d:
            print("k =", k)
            d = int(d)  # needed otherwise decryption goes wrong
            break
        else:
            k += 1
    '''  # this doesn't work
    d1, d2, g = gcd_euclid_ext(e, n)
    d = list(filter(lambda x: x>0, [d1, d2]))
    if g == 1 and len(d) == 1:
        d = d[0]
        print("Private key found,", d)
    else:
        print("Something went wrong, exiting.")
        return
    '''

    # encrypt and decrypt:
    enc_keys = [n, e]
    dec_keys = [n, d]
    print("Public key:", enc_keys)
    print("Private key:", dec_keys)
    message = int(input(f'For the message, enter an integer smaller than {n}: '))
    message_enc = message ** e % n
    message_dec = message_enc ** d % n
    print("Encrypted message:", message_enc)
    print("Decrypted message:", message_dec)


def crack_rsa():
    # find out p and q:
    pq = factorize(enc_keys[0])  # factorize n

    # find k such that (k * (p - 1) * (q - 1) + 1) is divisible by e, the quotient would then be d.
    while pq:
        p_test = min(pq)
        q_test = max(pq)

        k_test = 1
        while k < 65537 + 1:  # in practice is commonly 65537
            cond_test = k_test * (p_test - 1) * (q_test - 1) + 1
            if cond_test % e == 0:
                break
            else: k_test += 1

        d_guess = cond_test / e
        if d_guess != d:
            pq -= {p_test, q_test}
        elif d_guess == d:
            print("Private decoding key found:", d_guess)
            break


def main():
    use_rsa()

if __name__ == '__main__':
    main()