def precompute(prime, g, range_priv_keys):
    for a in range(*range_priv_keys):
        for b in range(*range_priv_keys):
            b_pub = g ** b % prime
            key = b_pub ** a % prime
            print(a, b, key)

def main():
    prime = int(input("Enter p in hex: "), base=16)
    g = int(input("Enter g in decimal: "))
    range_priv_keys = input(
        "Enter range of private keys to precompute for, separated by space: "
    )
    range_priv_keys = [int(n) for n in range_priv_keys.split()]
    precompute(prime, g, range_priv_keys)

if __name__ == '__main__':
    main()