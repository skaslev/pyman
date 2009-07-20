import unittest
from permutations import random_permutation,fract8_create

def is_perm(xs):
    return list(sorted(xs)) == list(range(len(xs)))

def is_perfect(k, x, y):
    assert len(x) == (1 << k) and len(y) == (1 << k)
    if k == 0: return x == [0] and y == [0]
    if set(x) != set(range(1 << k)) or set(y) != set(range(1 << k)): return False
    if k % 2 == 0:
        bucket_bits = k // 2
        bucket_points = 1
    else:
        bucket_bits = (k - 1) // 2
        bucket_points = 2
    buckets = {}
    for i in range(1 << k):
        b = ((x[i] >> (k - bucket_bits)) << bucket_bits) | (y[i] >> (k - bucket_bits))
        buckets[b] = buckets.setdefault(b, 0) + 1
    if len(buckets) != 1 << (2 * bucket_bits): return False
    if not all(v == bucket_points for v in buckets.values()): return False
    return is_perfect(k-1, [i >> 1 for i in x[:(1 << (k-1))]], [i >> 1 for i in y[:(1 << (k-1))]]) and \
           is_perfect(k-1, [i >> 1 for i in x[(1 << (k-1)):]], [i >> 1 for i in y[(1 << (k-1)):]])

class PermTest(unittest.TestCase):
    def test_is_perm(self):
        for i in range(100):
            xs = random_permutation(2**8)
            self.assertTrue(is_perm(xs))

class Fract8Test(unittest.TestCase):
    def test_is_perfect(self):
        for i in range(100):
            xs, ys = fract8_create()
            self.assertTrue(is_perfect(8, xs, ys))

if __name__ == '__main__':
    unittest.main()
