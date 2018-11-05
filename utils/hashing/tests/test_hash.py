from .. import hash_str

def test_hello_world():
    assert hash_str('world!', salt='hello, ').hex()[:6] == '68e656'


def test_byte_prefix():
    #  Make sure the hash can take a byte prefix
    CSCI_SALT = bytes.fromhex(
        "d4 b5 1b 2a 6c e0 2b b8 e8 29 ce 45 18 b0 f9 c0"
        "a8 f4 ec 6b 59 36 01 89 b1 be 69 26 1e 05 75 bc"
    )
    assert hash_str('world!', salt=CSCI_SALT).hex()
