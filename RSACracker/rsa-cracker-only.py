#!/usr/bin/python3

from rsa_cracker import crack_rsa

def main():
    e = int(input("e = "))
    n = int(input("n = "))
    cipher = int(input("cipher = "))
    crack_rsa((n, e), cipher)

if __name__ == '__main__':
    main()