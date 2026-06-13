
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
        return np.abs(H_z)

    def calc_angle_H(self, H_z):
        return np.angle(H_z)
