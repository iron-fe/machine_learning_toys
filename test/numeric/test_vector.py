import unittest
from src.numeric.vector import Vector


class VectorTest(unittest.TestCase):
    def test_init(self):
        print('=' * 25 + 'test_init' + '=' * 25)
        data = [[10, 20, 30], [4, 5, 6]]
        v = Vector(data)
        print(v)
        data = [[10, 2220, 300], [43, 5, 6]]
        v = Vector(data)
        print(v)

    def test_getitem(self):
        print('=' * 25 + 'test_getitem' + '=' * 25)
        data = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
        v = Vector(data)
        print(v[1])
        print(v[1, :, 1])
        print(v[1, 1, :])
        print(v[1, :])

    def test_setitem(self):
        print('=' * 25 + 'test_setitem' + '=' * 25)
        data = [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]]
        v = Vector(data)
        v[0,0,0] = 10
        print(v)
        v1 = Vector([[70, 80, 90], [100, 110, 120]])
        v[1] = v1
        print(v)
        v2 = Vector([123, 456])
        print(v[1, :, 1])
        v[1, :, 1] = v2
        print(v)

