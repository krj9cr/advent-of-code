# Note: to run this in PyCharm, set PYTHONENV=. as an environment variable,
#       which adds the current directory to be able to import Day21
from Day21 import get_tile, rock_to_tile

def test_get_tile():
    assert get_tile((0, 0), 11, 11) == (0, 0)
    assert get_tile((1, 1), 11, 11) == (0, 0)
    assert get_tile((1, 11), 11, 11) == (0, 1)
    assert get_tile((1, 15), 11, 11) == (0, 1)
    assert get_tile((1, 21), 11, 11) == (0, 1)
    assert get_tile((1, 22), 11, 11) == (0, 2)
    assert get_tile((11, 11), 11, 11) == (1, 1)
    assert get_tile((12, 12), 11, 11) == (1, 1)
    assert get_tile((12, 10), 11, 11) == (1, 0)
    assert get_tile((-1, 0), 11, 11) == (-1, 0)
    assert get_tile((-11, 0), 11, 11) == (-1, 0)
    assert get_tile((-12, 0), 11, 11) == (-2, 0)
    assert get_tile((0, -1), 11, 11) == (0, -1)
    assert get_tile((-1, -1), 11, 11) == (-1, -1)

def test_rock_to_tile():
    assert rock_to_tile((0, 0), (0, 0), 11, 11) == (0, 0)
    assert rock_to_tile((1, 1), (0, 0), 11, 11) == (1, 1)
    assert rock_to_tile((10, 10), (0, 0), 11, 11) == (10, 10)
    assert rock_to_tile((0, 0), (1, 0), 11, 11) == (11, 0)
    assert rock_to_tile((0, 0), (-1, -1), 11, 11) == (-11, -11)
    assert rock_to_tile((0, 0), (1, 1), 11, 11) == (11, 11)
