# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

from collections import Counter

import numpy as np


decimals = 6


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

        x = round(x, decimals)
        y = round(y, decimals)

        element = complex(x, y)

        if element.imag != 0:
            conj = complex(x, -y)
            self.list.append((element, conj))
        else:
            self.list.append((element,))

    def update_element(self, idx, x, y):
        x = round(x, decimals)
        y = round(y, decimals)

        pair = self.list[idx]

        if len(pair) == 2:
            p1 = complex(x, y)
            p2 = complex(x, -y)
            self.list[idx] = (p1, p2)
        else:
            p_real = complex(x, 0)
            self.list[idx] = (p_real,)

    def clear(self):
        self.list = []

    def empty(self):
        if self.list:
            return False
        return True

    def pop(self, idx):
        self.list.pop(idx)

    def _norm(self, list):
        list_norm = []
        for pair in list:
            pair_rounded = tuple(np.round(elem, decimals) for elem in pair)

            pair_sorted = tuple(
                sorted(
                    pair_rounded,
                    key=lambda c: (c.real, c.imag))  # first sort by real part
            )
            list_norm.append(pair_sorted)

        return Counter(list_norm)

    def equal(self, other):
        return self._norm(self.list) == self._norm(other.list)
