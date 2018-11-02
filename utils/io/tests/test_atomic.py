from .. import atomic_write
import os

def test_hello_world():
    with atomic_write("hello.txt") as f:
        f.write("world!")
    assert os.path.isfile('hello.txt')
    os.remove('hello.txt')


def test_partial_completion():
    try:
        with atomic_write("hello.txt") as f:
            f.write(True)
    except:
        assert not os.path.isfile('hello.txt')
