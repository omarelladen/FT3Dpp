# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import numpy as np
import sympy as sp
import scipy.signal as signal


# TODO: prevent -1 term instead of 1 in Y(z)
class MathUtils():
    def __init__(self, resolution, max_pi=1):
        self.resolution = resolution
        self.resolution_u = 0
        self.resolution_v = 0
        self.max_pi = max_pi

    def _get_w(self):
        return np.linspace(0, np.pi, self.resolution)

    def get_w_plot(self):
        return np.linspace(0, self.max_pi*np.pi, self.max_pi*self.resolution)

    def calc_H(self, zeros, poles):
        w = self._get_w()

        num = np.ones(self.resolution, dtype=complex)
        den = np.ones(self.resolution, dtype=complex)

        for pair_z in zeros.list:
            for zero in pair_z:
                num *= np.exp(1j*w) - zero
        for pair_p in poles.list:
            for pole in pair_p:
                den *= np.exp(1j*w) - pole

        with np.errstate(divide='ignore', invalid='ignore'):
            H_z = num / den  # den=0 => H_z=np.inf

        H_z = np.nan_to_num(H_z, nan=0.0, posinf=1e12, neginf=-1e12)
        return H_z

    def calc_mag_H(self, H_z):
        mag_base = np.abs(H_z)

        # [3,2,1,1,0] + [1,1,2] = [3,2,1,1,0,1,1,2,3] (e.g 500 pts -> 998 pts)
        mag_2pi = np.concatenate([mag_base, mag_base[::-1][1:-1]])

        num_rep = int(np.ceil(self.max_pi/2.0))  # repetitions of 2pi
        mag_total = np.tile(mag_2pi, num_rep)    # create repetition

        xp = np.linspace(0, num_rep*2.0*np.pi, len(mag_total))
        w_plot = self.get_w_plot()

        # Interpolate bc len(xp) != len(w_plot)
        mag_H = np.interp(w_plot, xp, mag_total)

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
        phase_base = np.angle(H_z)

        # [3,2,1,1,0] -> [3,2,1,1,0,-1,-1,-2,-3]
        phase_2pi = np.concatenate([phase_base, -phase_base[::-1][1:-1]])

        num_rep = int(np.ceil(self.max_pi/2.0))    # repetitions of 2pi
        phase_total = np.tile(phase_2pi, num_rep)  # create repetition

        xp = np.linspace(0, num_rep*2.0*np.pi, len(phase_total))
        w_plot = self.get_w_plot()

        # Interpolate bc len(xp) != len(w_plot)
        phase_final = np.interp(w_plot, xp, phase_total)

        return phase_final

    def calc_phase_H_deg(self, H_z):
        return np.rad2deg(self.calc_phase_H_rad(H_z))

    def calc_H_z_inv_eq(self, zeros, poles):
        num, den = self.calc_H_z_eq(zeros, poles)

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

    def calc_H_z_eq(self, zeros, poles):
        if not poles and not zeros:
            return 1, 1

        z = sp.symbols("z")

        num = 1
        den = 1

        for pair_z in zeros.list:
            for zero in pair_z:
                num *= z - sp.N(zero, 3)
        for pair_p in poles.list:
            for pole in pair_p:
                den *= z - sp.N(pole, 3)

        if num != 1:
            num = num.expand()
        if den != 1:
            den = den.expand()

        return num, den

    def calc_mag_H_3D(self, zeros, poles, clip_limit):
        u = np.linspace(0, 2*np.pi, self.resolution_u)
        v = np.linspace(0.01, 2.0, self.resolution_v)
        U, V = np.meshgrid(u, v)

        x_mesh = V*np.cos(U)
        y_mesh = V*np.sin(U)

        z_mesh = np.zeros_like(x_mesh)

        z_points = x_mesh + 1j*y_mesh

        num = np.ones_like(z_points, dtype=complex)
        den = np.ones_like(z_points, dtype=complex)

        for pair_z in zeros.list:
            for zero in pair_z:
                num *= z_points - zero

        for pair_p in poles.list:
            for pole in pair_p:
                den *= z_points - pole

        with np.errstate(divide='ignore', invalid='ignore'):
            H_z_mesh = num/den

        H_z_mesh = np.nan_to_num(H_z_mesh, nan=0.0, posinf=1e12, neginf=-1e12)

        z_mesh = np.abs(H_z_mesh)
        z_mesh = np.clip(z_mesh, None, clip_limit)

        return x_mesh, y_mesh, z_mesh

    def calc_line_3D(self, zeros, poles, clip_limit):
        w_plot = self.get_w_plot()
        H_z_line = self.calc_H(
            zeros,
            poles
        )

        z_line = self.calc_mag_H(H_z_line)
        z_line = np.clip(z_line, None, clip_limit)
        x_line = np.cos(w_plot)
        y_line = np.sin(w_plot)

        return x_line, y_line, z_line

    def tf2zpk(self, num, den):
        zeros, poles, gain = signal.tf2zpk(num, den)
        return zeros, poles, gain
