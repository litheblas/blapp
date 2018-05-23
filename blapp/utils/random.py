from binascii import hexlify
from os import urandom


def generate_random_hex_string(length):
    # Returns a random hex string, `length` characters long.
    return hexlify(urandom(length // 2 + (length % 2 > 0)))[0:length].decode()
