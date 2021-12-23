class Stack(object):
    def __init__(self):
        self.elems = []

    def pop(self):
        return self.elems.pop()

    def push(self, elem):
        self.elems.append(elem)

    def peek(self, level=-1):
        return self.elems[level]

    def stack_size(self):
        return len(self.elems)

    def __str__(self):
        s = '\n'.join(repr(ar) for ar in reversed(self.elems))
        s = f'CALL STACK\n{s}\n'
        return s

    __repr__ = __str__