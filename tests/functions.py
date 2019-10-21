import sys


def sum(a, b):
    return a + b

def product(a, b):
    return a * b

def all_branches_pass(condition):
    if condition == 1:
        return 20
    elif condition == 2:
        return 15
    else:
        return 10

def for_loop_passes(n):
    x = 0

    for i in range(n):
        x += i

    return x

def for_loop_skipped_passes(n):
    x = 0

    for i in range(n):
        x += i

    return x


def for_loop_skipped_fails(n):
    x = 0

    for i in range(n):
        x += i

    return x


def for_loop_fails(n):
    x = 0

    for i in range(n):
        x += i

    return x

def two_branch_fails(condition):
    if condition == 1:
        return 20
    elif condition == 2:
        raise Exception('Failure')
    else:
        raise Exception('Failure')

def untested():
    return 10

def fails():
    raise Exception('Failure')

class Dummy(object):
    def sum(self, a, b):
        return a + b

    def product(self, a, b):
        return a * b

    def all_branches_pass(self, condition):
        if condition == 1:
            return 20
        elif condition == 2:
            return 15
        else:
            return 10

    def two_branch_fails(self, condition):
        if condition == 1:
            return 20
        elif condition == 2:
            raise Exception('Failure')
        else:
            raise Exception('Failure')

    def for_loop_passes(self, n):
        x = 0

        for i in range(n):
            x += i

        return x

    def for_loop_skipped_passes(self, n):
        x = 0

        for i in range(n):
            x += i

        return x


    def for_loop_skipped_fails(self, n):
        x = 0

        for i in range(n):
            x += i

        return x

    def for_loop_fails(self, n):
        x = 0

        for i in range(n):
            x += i

        return x

    def untested(self):
        return 10

    def fails(self):
        raise Exception('Failure')
