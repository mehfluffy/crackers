def factorize(n):
    factors = [[i, n//i] for i in range(2, int(n**0.5)+1) if n%i==0]  # ignore 1 & n, square root = largest factor
    return set(reduce(list.__add__, factors))  # flatten and make into set (faster, no repeated square roots)


def factorize_sieve(n):
    # initialize sieve
    limit = int(n**0.5 + 1)  # iterate till largest integer smaller than sqrt(n)
    sieve = [False, False, True, True]  # 0,1,2,3
    while len(sieve) < limit:
        sieve.append(False)  # filter even numbers
        sieve.append(True)
    
    # check odd numbers
    for i in range(5, len(sieve)):
        if sieve[i] == True:
            j = i * i  # avoids checking double, which j=i*2 would do
            while j < len(sieve):
                sieve[j] = False
                j += i
    
    # check if biggest prime is factor of n, if not, check next biggest
    while sieve:
        if sieve[-1]:
            p_try = len(sieve) - 1
            q = n / p_try
            if int(q) == q:
                return p_try, int(q)
        sieve.pop(-1)