from functools import reduce
from numpy import lcm, gcd

def factorize(n):    
    factors = set(
        reduce(
            list.__add__,
            ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)
        )
    )
    factors -= {1, max(factors)}  # remove 1 and n
    if len(factors) == 1:  # what if odd number of factors instead of just one
        factors = list(factors) * 2
    return factors


# choose p and q:
p = int(input("Enter prime 1: "))
q = int(input("Enter prime 2, different from prime 1: "))
n = p * q

# choose k:
l = lcm(p - 1, q - 1)
k_choices = []
for i in range(1, l):
    if gcd(i, l) == 1:
        k_choices.append(i)
if len(k_choices) > 1:
    k = int(input(f"Choose k as one of {k_choices}:"))
else: 
    k = k_choices[0]
    print("Only 1 choice for e found, using:", k)

# choose e and d:
cond = k * (p - 1) * (q - 1) + 1   # = e * d

print(factorize(cond))
e, d = factorize(cond)  # not always just 2 factors.
# d is determined differently at https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation

# encrypt and decrypt:
enc_keys = [n, e]
dec_keys = [n, d]
print("Public key:", enc_keys)
message = int(input(f'Enter an integer smaller than {n}: '))
message_enc = message ** e % n
message_dec = message_enc ** d % n
print("Decoded message:", message_dec)


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
