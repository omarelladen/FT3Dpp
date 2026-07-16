# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

class Elements():
    def __init__(self, type):
        self.list: list[tuple(complex, complex)] = []
        self.type: str = type

    def num_elements(self):
        return sum(len(pair) for pair in self.list)

    def num_pairs(self):
        return len(self.list)

    def add(self, x, y):
        '''Called only once for each complex conjugate pair'''
        # TODO: truncate floats
        element = complex(x, y)
        if element.imag != 0:
            conj = complex(x, -y)
            self.list.append((element, conj))
        else:
            self.list.append((element,))

    def clear(self):
        self.list = []

    def empty(self):
        if self.list:
            return False
        return True

    def pop(self, idx):
        self.list.pop(idx)
