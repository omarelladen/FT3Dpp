# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

from collections import Counter

import numpy as np


decimals = 6


class Elements():
    def __init__(self, type_el):
        self.list_el: list[tuple(complex, complex)] = []
        self.type_el: str = type_el

    def num_elements(self):
        return sum(len(pair) for pair in self.list_el)

    def num_pairs(self):
        return len(self.list_el)

    def add(self, x, y):
        """Called only once for each complex conjugate pair"""

        x = round(x, decimals)
        y = round(y, decimals)

        element = complex(x, y)

        if element.imag != 0:
            conj = complex(x, -y)
            self.list_el.append((element, conj))
        else:
            self.list_el.append((element,))

    def update_element(self, idx, x, y):
        x = round(x, decimals)
        y = round(y, decimals)

        if y == 0:  # real
            p = complex(x, 0)
            self.list_el[idx] = (p,)
        else:
            p1 = complex(x, y)
            p2 = complex(x, -y)
            self.list_el[idx] = (p1, p2)

    def clear(self):
        self.list_el = []

    def empty(self):
        if self.list_el:
            return False
        return True

    def pop(self, idx):
        self.list_el.pop(idx)

    def _norm(self, list_el):
        list_norm = []
        for pair in list_el:
            pair_rounded = tuple(np.round(elem, decimals) for elem in pair)

            pair_sorted = tuple(
                sorted(
                    pair_rounded,
                    key=lambda c: (c.real, c.imag))  # first sort by real part
            )
            list_norm.append(pair_sorted)

        return Counter(list_norm)

    def __eq__(self, other):
        return self._norm(self.list_el) == self._norm(other.list_el)
