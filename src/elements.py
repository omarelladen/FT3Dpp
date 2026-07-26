# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

from collections import Counter

import numpy as np


decimals = 6


class Elements():
    def __init__(self, type_):
        self.list_: list[tuple(complex, complex)] = []
        self.type_: str = type

    def num_elements(self):
        return sum(len(pair) for pair in self.list_)

    def num_pairs(self):
        return len(self.list_)

    def add(self, x, y):
        """Called only once for each complex conjugate pair"""

        x = round(x, decimals)
        y = round(y, decimals)

        element = complex(x, y)

        if element.imag != 0:
            conj = complex(x, -y)
            self.list_.append((element, conj))
        else:
            self.list_.append((element,))

    def update_element(self, idx, x, y):
        x = round(x, decimals)
        y = round(y, decimals)

        if y == 0:  # real
            p = complex(x, 0)
            self.list_[idx] = (p,)
        else:
            p1 = complex(x, y)
            p2 = complex(x, -y)
            self.list_[idx] = (p1, p2)

    def clear(self):
        self.list_ = []

    def empty(self):
        if self.list_:
            return False
        return True

    def pop(self, idx):
        self.list_.pop(idx)

    def _norm(self, list_):
        list_norm = []
        for pair in list_:
            pair_rounded = tuple(np.round(elem, decimals) for elem in pair)

            pair_sorted = tuple(
                sorted(
                    pair_rounded,
                    key=lambda c: (c.real, c.imag))  # first sort by real part
            )
            list_norm.append(pair_sorted)

        return Counter(list_norm)

    def __eq__(self, other):
        return self._norm(self.list_) == self._norm(other.list_)
