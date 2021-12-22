class Stack(object):
    def __init__(self):
        self.elems = []

    def pop(self):
        return self.elems.pop()

    def push(self, elem):
        self.elems.append(elem)

    def peek(self):
        return self.elems[-1]

    def __str__(self):
        s = '\n'.join(repr(ar) for ar in reversed(self.elems))
        s = f'CALL STACK\n{s}\n'
        return s

    __repr__ = __str__