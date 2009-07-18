def left_most_bit(n):
    assert n < (1 << 31)

    if n == 0:
        return -1

    ret,b = 0,16
    while b:
        if n >> b != 0:
            ret += b
            n >>= b
        b >>= 1
    return ret
