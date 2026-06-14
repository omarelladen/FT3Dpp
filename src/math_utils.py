
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

        for tuple_zero in list_zeros:
            zero = tuple_zero[0] + 1j*tuple_zero[1]
            num *= np.exp(1j*w) - zero
        for tuple_pole in list_poles:
            pole = tuple_pole[0] + 1j*tuple_pole[1]
            den *= np.exp(1j*w) - pole

        H_z = num/den
        return H_z

    def calc_abs_H(self, H_z):
        abs_H = np.abs(H_z)
        abs_H = np.clip(abs_H, a_min=1e-12, a_max=None)
        return abs_H

    def calc_abs_H_db(self, H_z):
        abs_H = self.calc_abs_H(H_z)
        abs_H_db = 20 * np.log10(abs_H)
        return abs_H_db

    def calc_abs_H_norm(self, H_z):
        abs_H = self.calc_abs_H(H_z)
        peak = np.max(abs_H)
        if peak > 0:
            abs_H = abs_H / peak
        return abs_H

    def calc_abs_H_db_norm(self, H_z):
        abs_H_db = self.calc_abs_H_db(H_z)
        peak = np.max(abs_H_db)
        abs_H_db = abs_H_db - peak
        return abs_H_db

    def calc_angle_H(self, H_z):
        return np.angle(H_z)

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

        for tuple_zero in list_zeros:
            zero = tuple_zero[0] + 1j*tuple_zero[1]
            num *= z - sp.N(zero, 3)

        for tuple_pole in list_poles:
            pole = tuple_pole[0] + 1j*tuple_pole[1]
            den *= z - sp.N(pole, 3)

        if num != 1:
            num = num.expand()
        if den != 1:
            den = den.expand()

        return num, den

    def format_H_z_inv(self, list_zeros, list_poles):
        num, den = self._calc_H_z_inv_eq(list_zeros, list_poles)

        if num == 1 and den == 1:
            return "H(z) = 1"

        num = str(num)
        den = str(den)

        # Substitutions

        for exp in range(max_exp, 1, -1):
            new_exp = "⁻" + "".join(dict_subst_exp[d] for d in str(exp))
            num = num.replace(f"z_inv**{exp}", f"z{new_exp}")
            den = den.replace(f"z_inv**{exp}", f"z{new_exp}")

        for old, new in dict_subst_z.items():
            num = num.replace(old, new)
            den = den.replace(old, new)

        eq = self._create_eq(num, den)
        return eq

    def format_H_z(self, list_zeros, list_poles):
        num, den = self._calc_H_z_eq(list_zeros, list_poles)

        if num == 1 and den == 1:
            return "H(z) = 1"

        num = str(num)
        den = str(den)

        # Substitutions

        for exp in range(max_exp, 1, -1):
            new_exp = "".join(dict_subst_exp[d] for d in str(exp))
            num = num.replace(f"z**{exp}", f"z{new_exp}")
            den = den.replace(f"z**{exp}", f"z{new_exp}")

        for old, new in dict_subst_z.items():
            num = num.replace(old, new)
            den = den.replace(old, new)

        eq = self._create_eq(num, den)
        return eq

    def _create_eq(self, num, den):
        bar_size = max(len(num), len(den))
        bar = "—" * bar_size

        num_center = num.center(bar_size)
        den_center = den.center(bar_size)

        eq = (
            f"       {num_center}\n"
            f"H(z) = {bar}\n"
            f"       {den_center}"
        )
        return eq
