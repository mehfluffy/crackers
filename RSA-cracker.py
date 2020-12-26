#!/usr/bin/env python

from functools import reduce

def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


# params:
p = 7; q = 13; k = 2   # these can be user defined
n = p * q
cond = k * (p - 1) * (q - 1) + 1   # = e * d
cond_factors = factors(cond)       
e, d = cond_factors - {1, max(cond_factors)}  # remove 1 and itself from factors

# encrypt and decrypt:
enc_keys = [n, e]   # can print for the user
dec_keys = [n, d]
message = int(input('Enter an integer: '))
message_enc = message ** e % n
message_dec = message_enc ** d % n
print(message_dec == message)

# find out p and q:
print(factors(n))
# find k such that (k * (p - 1) * (q - 1) + 1) is divisible by e, the quotient would then be d.
