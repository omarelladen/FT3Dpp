# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import numpy as np
import sympy as sp


dict_subst_exp = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
}
dict_subst_z = {
    "z_inv": "z⁻¹",
    "*": "",
    "1.0z": "z",
    "z⁻¹ + 1.0": "z⁻¹ + 1",
    " ": ""
}

max_exp = 20


# TODO: prevent RuntimeWarning: divide by zero encountered in divide
#               RuntimeWarning: invalid value  encountered in divide
class MathUtils():
    def __init__(self, resolution, max_pi):
        self.resolution = resolution
        self.max_pi = max_pi

    def get_w(self):
        return np.linspace(0, self.max_pi*np.pi, self.resolution)

    def calc_H(self, list_zeros, list_poles):
        w = self.get_w()

        num = np.ones(self.resolution, dtype=complex)
        den = np.ones(self.resolution, dtype=complex)

        for i in range(0, len(list_zeros), 2):
            if i + 1 < len(list_zeros):
                tuple_z1 = list_zeros[i]
                tuple_z2 = list_zeros[i+1]
                z1 = tuple_z1[0] + 1j*tuple_z1[1]
                z2 = tuple_z2[0] + 1j*tuple_z2[1]
                num *= np.exp(1j*w) - z1
                if z1 != z2:  # conj
                    num *= np.exp(1j*w) - z2
        for i in range(0, len(list_poles), 2):
            if i + 1 < len(list_poles):
                tuple_p1 = list_poles[i]
                tuple_p2 = list_poles[i+1]
                p1 = tuple_p1[0] + 1j*tuple_p1[1]
                p2 = tuple_p2[0] + 1j*tuple_p2[1]
                den *= np.exp(1j*w) - p1
                if p1 != p2:  # conj
                    den *= np.exp(1j*w) - p2

        H_z = num/den
        return H_z

    def calc_mag_H(self, H_z):
        mag_H = np.abs(H_z)
        mag_H = np.clip(mag_H, a_min=1e-12, a_max=None)
        return mag_H

    def calc_mag_H_db(self, H_z):
        mag_H = self.calc_mag_H(H_z)
        mag_H_db = 20 * np.log10(mag_H)
        return mag_H_db

    def calc_mag_H_norm(self, H_z):
        mag_H = self.calc_mag_H(H_z)
        peak = np.max(mag_H)
        if peak > 0:
            mag_H = mag_H/peak
        return mag_H

    def calc_mag_H_db_norm(self, H_z):
        mag_H_db = self.calc_mag_H_db(H_z)
        peak = np.max(mag_H_db)
        mag_H_db = mag_H_db - peak
        return mag_H_db

    def calc_phase_H_rad(self, H_z):
        return np.angle(H_z)

    def calc_phase_H_deg(self, H_z):
        return np.rad2deg(self.calc_phase_H_rad(H_z))

    def _calc_H_z_inv_eq(self, list_zeros, list_poles):
        num, den = self._calc_H_z_eq(list_zeros, list_poles)

        if num == 1 and den == 1:
            return 1, 1

        z     = sp.symbols("z")
        z_inv = sp.symbols("z_inv")

        H_z = num/den

        # Replace z with 1/z_inv
        H_z_inv = H_z.subs(z, 1/z_inv).cancel()
        num, den = H_z_inv.as_numer_denom()

        num = sp.expand(num)
        den = sp.expand(den)

        return num, den

    def _calc_H_z_eq(self, list_zeros, list_poles):
        if not list_poles and not list_zeros:
            return 1, 1

        z = sp.symbols("z")

        num = 1
        den = 1

        for i in range(0, len(list_zeros), 2):
            if i + 1 < len(list_zeros):
                tuple_z1 = list_zeros[i]
                tuple_z2 = list_zeros[i+1]
                z1 = tuple_z1[0] + 1j*tuple_z1[1]
                z2 = tuple_z2[0] + 1j*tuple_z2[1]
                num *= z - sp.N(z1, 3)
                if z1 != z2:  # conj
                    num *= z - sp.N(z2, 3)
        for i in range(0, len(list_poles), 2):
            if i + 1 < len(list_poles):
                tuple_p1 = list_poles[i]
                tuple_p2 = list_poles[i+1]
                p1 = tuple_p1[0] + 1j*tuple_p1[1]
                p2 = tuple_p2[0] + 1j*tuple_p2[1]
                den *= z - sp.N(p1, 3)
                if p1 != p2:  # conj
                    den *= z - sp.N(p2, 3)

        if num != 1:
            num = num.expand()
        if den != 1:
            den = den.expand()

        return num, den

    def format_H_z_inv(self, list_zeros, list_poles):
        return self._format_H_z(
            list_zeros,
            list_poles,
            self._calc_H_z_inv_eq,
            "⁻",
            "z_inv"
        )

    def format_H_z(self, list_zeros, list_poles):
        return self._format_H_z(
            list_zeros,
            list_poles,
            self._calc_H_z_eq,
            "",
            "z"
        )

    def _format_H_z(self, list_zeros, list_poles, funct, signal, base):
        num, den = funct(list_zeros, list_poles)

        if num == 1 and den == 1:
            return "H(z) = 1"

        num = str(num)
        den = str(den)

        # Substitutions

        for exp in range(max_exp, 1, -1):
            new_exp = signal + "".join(dict_subst_exp[d] for d in str(exp))
            num = num.replace(f"{base}**{exp}", f"z{new_exp}")
            den = den.replace(f"{base}**{exp}", f"z{new_exp}")

        for old, new in dict_subst_z.items():
            num = num.replace(old, new)
            den = den.replace(old, new)

        return self._create_eq(num, den)

    def _create_eq(self, num, den):
        bar_size = max(len(num), len(den))
        bar = "—" * bar_size

        num_center = num.center(bar_size)
        den_center = den.center(bar_size)

        return (
            f"       {num_center}\n"
            f"H(z) = {bar}\n"
            f"       {den_center}"
        )
