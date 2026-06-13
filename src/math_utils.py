
import numpy as np


class MathUtils():
    def __init__(self, resolution):
        self.resolution = resolution

    def get_w(self):
        return np.linspace(0, 4*np.pi, self.resolution)

    def calc_H(self, list_zeros, list_poles):
        w = self.get_w()

        num = np.ones(self.resolution, dtype=complex)
        den = np.ones(self.resolution, dtype=complex)

        for tuple_zero in list_zeros:
            zero = tuple_zero[0] + 1j*tuple_zero[1]
            num *= np.exp(1j*w) - zero
            print(zero)
        print()

        for tuple_pole in list_poles:
            pole = tuple_pole[0] + 1j*tuple_pole[1]
            den *= np.exp(1j*w) - pole
            print(pole)
        print()
        print()

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
