#!/usr/bin/python3


from functools import reduce
from math import gcd  #lcm only in 3.9+


def lcm(a, b):
    return (a*b) // gcd(a, b)


def factorize(n):
    factors = [[i, n//i] for i in range(2, int(n**0.5)+1) if n%i==0]  # ignore 1 & n, square root = largest factor
    return set(reduce(list.__add__, factors))  # flatten and make into set (faster, no repeated square roots)


def crack_rsa(e, n, message_enc):
    print("CRACKING RSA:")
    # by factorizing n:
    pq = factorize(n)
    print("Factors of n found:", pq)

    # find k such that (1+k*lambda) is divisible by e, the quotient would then be d.
    while pq:
        p_test = min(pq)
        q_test = max(pq)
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
    e = int(input("e = "))
    n = int(input("n = "))
    cipher = int(input("cipher = "))
    crack_rsa(e, n, cipher)

if __name__ == '__main__':
    main()