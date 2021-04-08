from math import sqrt
import itertools

def is_prime(n):
    if n < 2:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    i = 2
    end = sqrt(n) + 1
    while i < end:
        if n % i == 0:
            return False
        i += 1
    return True


def split_seq(iterable, size):
    it = iter(iterable)
    while item := list(itertools.islice(it, size)):
        yield item


def create_lists(iterable, num_per_list):
    return list(split_seq(iterable, num_per_list))


