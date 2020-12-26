import hashlib
import numpy as np

passwords = np.core.defchararray.array(
    np.loadtxt('top-10000-passwords.txt', dtype='str')
)  # needed for vectorized operations with salt string

salts = np.loadtxt('known-salts.txt', dtype='str')


def sha1_digest(string):
    return hashlib.sha1(str.encode(string)).hexdigest()

def md5_digest(string):
    return hashlib.md5(str.encode(string)).hexdigest()

def hash_digest_list(arr, algo):
    '''
    Returns the hashes of a list (arr) of strings,
    hashed with the specified algorithm (algo), 
    algo must be either 'SHA1' or 'MD5'.
    '''
    if algo == 'SHA1':
        func = sha1_digest
    if algo == 'MD5':
        func = md5_digest
    return [func(string) for string in arr]

def crack_sha1_hash(hash, use_salts=False, algo='SHA1'):
    '''
    Takes hash and compares it with the hashes of the top 10000 
    passwords, hashed with the specified algorithm.
    If use_salts == True, compares with hashes of salt-prepended 
    and salt-appended passwords.
    Returns the unhashed password or "Password not in database".
    '''
    if use_salts:
        salted_hashes = np.array([[
                hash_digest_list(salt + passwords, algo), 
                hash_digest_list(passwords + salt, algo)
            ] for salt in salts
        ])  # has shape (len(salts), 2, (len(passwords)))
        match = passwords[np.where(salted_hashes == hash)[2]]
    else:
        hashes = np.array(hash_digest_list(passwords, algo))
        match = passwords[np.where(hashes == hash)]
    if match:
        return match
    else: return "PASSWORD NOT IN DATABASE"