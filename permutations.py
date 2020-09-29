from __future__ import division
from random import shuffle, randrange


def random_permutation(n):
    ret = list(range(n))
    shuffle(ret)
    return ret


def hammersley(k):
    if k == 0:
        return [0]
    return [(i << 1) | 0 for i in hammersley(k-1)] + [(i << 1) | 1 for i in hammersley(k-1)]


f8xs = hammersley(8)
f8ys = [25, 153, 217, 89, 121, 249, 185, 57, 137, 9, 73, 201, 233, 105, 41, 169, 113, 241, 177, 49, 17, 145, 209, 81, 225, 97, 33, 161, 129, 1, 65, 193, 189, 61, 125, 253, 93, 221, 157, 29, 45, 173, 237, 109, 205, 77, 13, 141, 85, 213, 149, 21, 53, 181, 245, 117, 197, 69, 5, 133, 165, 37, 101, 229, 239, 111, 47, 175, 143, 15, 79, 207, 127, 255, 191, 63, 31, 159, 223, 95, 39, 167, 231, 103, 71, 199, 135, 7, 183, 55, 119, 247, 215, 87, 23, 151, 203, 75, 11, 139, 43, 171, 235, 107, 155, 27, 91, 219, 123, 251, 187, 59, 67, 195, 131, 3, 163, 35, 99, 227, 19, 147, 211, 83, 243, 115, 51, 179, 110, 238, 174, 46, 14, 142, 206, 78, 222, 94, 30, 158, 190, 62, 126, 254, 134, 6, 70, 198, 230, 102, 38, 166, 54, 182, 246, 118, 86, 214, 150, 22, 162, 34, 98, 226, 194, 66, 2, 130, 82, 210, 146, 18, 50, 178, 242, 114, 10, 138, 202, 74, 106, 234, 170, 42, 250, 122, 58, 186, 154, 26, 90, 218, 208, 80, 16, 144, 176, 48, 112, 240, 96, 224, 160, 32, 0, 128, 192, 64, 56, 184, 248, 120, 216, 88, 24, 152, 168, 40, 104, 232, 72, 200, 136, 8, 148, 20, 84, 212, 244, 116, 52, 180, 68, 196, 132, 4, 36, 164, 228, 100, 252, 124, 60, 188, 156, 28, 92, 220, 12, 140, 204, 76, 108, 236, 172, 44]

# THE FOLLOWING CODE IS PORTED FROM C

K = 8
N = 2 ** K


# The quality of the sequences generated doesn't depend much on the RNG used,
# so feel free to plug your favourite here.
# Also note that this function is the only source of nondeterminism.
# rand_bit      returns 0 or 1
def randbit():
    return randrange(2)


# Makes random swaps over the permutation xs which keep it's fractality. It
# only affects the lower K/2 bits of xs elements, so it doesn't degrade the
# discrepancy.
# The complexity of the algorithm is O(N log(N)).
def scramble(xs):
    for i in range(K//2):
        length = 2 ** (K - i)
        q = 2 ** (i + 1)
        for offs in range(0, N, length):
            inv = [0] * (N // 2)
            for j in range(offs, offs + length // 2):
                inv[xs[j] // q] = j

            for j in range(offs + length // 2, offs + length):
                if randbit():
                    j2 = inv[xs[j] // q]
                    xs[j], xs[j2] = xs[j2], xs[j]


def reverse(xs, offs, length):
    i, j = offs, offs+length-1
    while i < j:
        xs[i], xs[j] = xs[j], xs[i]
        i += 1
        j -= 1


# Makes random reverses over xs and ys. It keeps the points untouched and
# chages only their order while keeping xs and ys fractal.
# The complexity is O(N log(N)).
def reorder(xs, ys):
    length = N
    while length > 1:
        for offs in range(0, N, length):
            if randbit():
                reverse(xs, offs, length)
                reverse(ys, offs, length)
        length //= 2


def fract8_create():
    xs, ys = f8xs[:], f8ys[:]
    scramble(xs)
    scramble(ys)
    reorder(xs, ys)
    return (xs, ys)
