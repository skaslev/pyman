from random import shuffle

def random_permutation(n):
    ret = list(range(n))
    shuffle(ret)
    return ret
