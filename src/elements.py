# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

from collections import Counter

import numpy as np


class Elements():
    def __init__(self, type):
        self.list: list[tuple(complex, complex)] = []
        self.type: str = type

    def num_elements(self):
        return sum(len(pair) for pair in self.list)

    def num_pairs(self):
        return len(self.list)

    def add(self, x, y):
        """Called only once for each complex conjugate pair"""
        # TODO: truncate floats and see decimals in _norm
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

    def _norm(self, list, decimals=3):
        list_norm = []
        for pair in list:
            pair_rounded = tuple(np.round(val, decimals) for val in pair)

            pair_sorted = tuple(
                sorted(
                    pair_rounded,
                    key=lambda c: (c.real, c.imag))  # first sort by real part
            )
            list_norm.append(pair_sorted)

        return Counter(list_norm)

    def equal(self, other):
        return self._norm(self.list) == self._norm(other.list)
