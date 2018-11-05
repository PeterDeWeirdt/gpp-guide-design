import hashlib

def hash_str(some_str, salt=''):
    """Implement a standardized string hash

    :param some_str: string
    :param salt: prefix to increase randomness
    :return: .digest() of the hash as a bytes array
    """
    m = hashlib.sha256()
    if type(salt) == str:
        salt = salt.encode()
    m.update(salt) #Unicode-objects must be encoded before hashing
    m.update(some_str.encode())
    return m.digest()
