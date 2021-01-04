from functools import reduce
from math import gcd, floor #lcm only in 3.9+


def lcm(a, b):
    return (a*b) // gcd(a, b)


def factorize(n):    
    factors = [[i, n//i] for i in range(2, int(n**0.5)+1) if n%i==0]   # square root = biggest factor
    return set(reduce(list.__add__, factors)) # flatten and make into set (faster, no repeated element)


def use_rsa():
    print("USING RSA:")

    # choose p and q:
    p = int(input("Enter prime 1: "))
    q = int(input("Enter prime 2, different from prime 1: "))
    n = p * q

    # compute phi and lambda:
    phi = (p-1) * (q-1)
    lam = lcm(p - 1, q - 1)

    # choose e:
    e_choices = []
    for i in range(1, lam):
        if gcd(i, lam) == 1:
            e_choices.append(i)
    if len(e_choices) > 1:
        e = int(input(f"Choose e as one of {e_choices}: "))
    elif len(e_choices) == 1:
        e = e_choices[0]
        print("Only 1 choice for e found, using:", e)
    else:
        print("No choices for e found, please choose bigger primes for p and q.")
        return

    # compute d:
    k = 1
    while k > 0:
        d = (1 + k*lam) / e
        if floor(d) == d:
            d = int(d)  # needed otherwise decryption goes wrong
            break
        else:
            k += 1

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

    return enc_keys, message_enc


def crack_rsa(enc_keys, message_enc):
    print("CRACKING RSA:")
    n, e = enc_keys
    # by factorizing n:
    pq = factorize(n)
    print("Factors of n found:", pq)

    # find k such that (k * (p - 1) * (q - 1) + 1) is divisible by e, the quotient would then be d.
    while pq:
        p_test = min(pq)
        q_test = max(pq)
        #phi_test = (p_test-1) * (q_test-1)
        lam_test = lcm(p_test-1, q_test-1)

        k_test = 1
        while k_test > 0:
            test = 1 + k_test * lam_test
            if test % e == 0:
                break  # inner loop
            else: k_test += 1
        
        d_guess = int(test / e)  # integer since test % e == 0
        message_dec = message_enc ** d_guess % n
        print("Private key found:", d_guess)
        print("Decrypted message:", message_dec)
        break
        '''
        if d_guess != d:
            pq -= {p_test, q_test}
        elif d_guess == d:
            print("Private key found:", d_guess)
            break
        '''


def main():
    enc_keys, message_enc = use_rsa()
    resp = input("Attempt to crack encryption? [y/n]: ")
    if resp == 'y':
        crack_rsa(enc_keys, message_enc)

if __name__ == '__main__':
    main()