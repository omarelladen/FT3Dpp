# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import numpy as np
import scipy.signal as signal


max_value = 1e12
min_value = 1e-12

decimals = 3


# TODO: prevent -1 term instead of 1 in Y(z)
#       1.0 -> 1
#       update imp e step resp on clear (update_all)
class MathUtils():
    def __init__(self, resolution, sample_size, max_pi=1):
        self.resolution = resolution
        self.resolution_u = 0
        self.resolution_v = 0
        self.clip_limit_3d = 0
        self.sample_size = sample_size
        self.max_pi = max_pi

        self.sys_dlti = None
        self.tf = None

    def update_sys(self, zeros, poles, gain=1):
        self.sys_dlti = self.dlti(zeros, poles, gain=gain)
        self.tf = signal.TransferFunction(self.sys_dlti)

    def _w(self):
        return np.linspace(0, np.pi, self.resolution)

    def w_plot(self):
        return np.linspace(0, self.max_pi*np.pi, self.max_pi*self.resolution)

    def H_jw(self, zeros, poles):
        w = self._w()

        num = np.ones(self.resolution, dtype=complex)
        den = np.ones(self.resolution, dtype=complex)

        for pair in zeros.list:
            for zero in pair:
                num *= np.exp(1j*w) - zero
        for pair in poles.list:
            for pole in pair:
                den *= np.exp(1j*w) - pole

        with np.errstate(divide="ignore", invalid="ignore"):
            H_jw = num / den  # den=0 => H_jw=np.inf

        H_jw = np.nan_to_num(H_jw, nan=0.0, posinf=max_value, neginf=-max_value)
        return H_jw

    def mag_H_jw(self, H_jw):
        mag_base = np.abs(H_jw)

        # [3,2,1,1,0] + [1,1,2] = [3,2,1,1,0,1,1,2,3] (e.g 500 pts -> 998 pts)
        mag_2pi = np.concatenate([mag_base, mag_base[::-1][1:-1]])

        num_rep = int(np.ceil(self.max_pi/2.0))  # repetitions of 2pi
        mag_total = np.tile(mag_2pi, num_rep)    # create repetition

        xp = np.linspace(0, num_rep*2.0*np.pi, len(mag_total))
        w_plot = self.w_plot()

        # Interpolate bc len(xp) != len(w_plot)
        mag_H_jw = np.interp(w_plot, xp, mag_total)

        mag_H_jw = np.clip(mag_H_jw, a_min=min_value, a_max=None)

        return mag_H_jw

    def mag_H_jw_db(self, H_jw):
        mag_H_jw = self.mag_H_jw(H_jw)
        mag_H_jw_db = 20 * np.log10(mag_H_jw)
        return mag_H_jw_db

    def mag_H_jw_norm(self, H_jw):
        mag_H_jw = self.mag_H_jw(H_jw)
        peak = np.max(mag_H_jw)
        if peak > 0:
            mag_H_jw = mag_H_jw/peak
        return mag_H_jw

    def mag_H_jw_db_norm(self, H_jw):
        mag_H_jw_db = self.mag_H_jw_db(H_jw)
        peak = np.max(mag_H_jw_db)
        mag_H_jw_db = mag_H_jw_db - peak
        return mag_H_jw_db

    def phase_H_rad(self, H_jw):
        phase_base = np.angle(H_jw)

        # [3,2,1,1,0] -> [3,2,1,1,0,-1,-1,-2,-3]
        phase_2pi = np.concatenate([phase_base, -phase_base[::-1][1:-1]])

        num_rep = int(np.ceil(self.max_pi/2.0))    # repetitions of 2pi
        phase_total = np.tile(phase_2pi, num_rep)  # create repetition

        xp = np.linspace(0, num_rep*2.0*np.pi, len(phase_total))
        w_plot = self.w_plot()

        # Interpolate bc len(xp) != len(w_plot)
        phase = np.interp(w_plot, xp, phase_total)

        # Clip both min_value and -min_value to 0
        phase[np.abs(phase) < min_value] = 0

        return phase

    def phase_H_deg(self, H_jw):
        return np.rad2deg(self.phase_H_rad(H_jw))

    def H_z_inv_sym(self, zeros, poles):
        if not poles and not zeros:
            return "1", "1"

        self.H_z_sym(zeros, poles)  ####### tf was None

        num = list(self.tf.num)
        den = list(self.tf.den)

        # Zero pad the smaller
        diff = len(num) - len(den)
        if diff < 0:
            num = [0]*abs(diff) + num
        elif diff > 0:
            den = [0]*diff + den

        num.reverse()
        den.reverse()

        num_str = self._format_coefs_sym(num, "z_inv")
        den_str = self._format_coefs_sym(den, "z_inv")

        return num_str, den_str

    def _format_coefs_sym(self, list, sym):
        is_first = True
        str = ""
        for i, coef in enumerate(list):
            list_degree = len(list) - 1
            coef_degree = list_degree - i

            if coef == 0:
                continue
            if coef > 0:
                if is_first:
                    sign = ""
                else:
                    sign = "+"
            else:
                sign = ""

            is_first = False

            coef_round = round(coef, 3)
            if coef_degree == 0:
                str += f"{sign}{coef_round}"
            elif coef_degree == 1:
                str += f"{sign}{coef_round}*{sym}"
            else:
                str += f"{sign}{coef_round}*{sym}**{coef_degree}"

        return str

    def H_z_sym(self, zeros, poles):
        if not poles and not zeros:
            return "1", "1"

        num_str = self._format_coefs_sym(self.tf.num, "z")
        den_str = self._format_coefs_sym(self.tf.den, "z")

        return num_str, den_str

    def _H_z_3D(self, zeros, poles, z):
        num = np.ones_like(z, dtype=complex)
        den = np.ones_like(z, dtype=complex)

        for pair in zeros.list:
            for zero in pair:
                num *= z - zero

        for pair in poles.list:
            for pole in pair:
                den *= z - pole

        with np.errstate(divide="ignore", invalid="ignore"):
            H_z = num/den

        H_z = np.nan_to_num(H_z, nan=0.0, posinf=max_value, neginf=-max_value)

        return H_z

    def mag_H_z_3D(self, zeros, poles, clip_limit):
        u = np.linspace(0, 2*np.pi, self.resolution_u)
        v = np.linspace(0.01, 2.0, self.resolution_v)
        U, V = np.meshgrid(u, v)

        x = V*np.cos(U)
        y = V*np.sin(U)

        H_z = self._H_z_3D(zeros, poles, z=x+1j*y)

        z = np.abs(H_z)
        z = np.clip(z, a_min=None, a_max=clip_limit)

        return x, y, z

    def mag_H_jw_3D(self, zeros, poles, clip_limit):
        w_plot = self.w_plot()

        H_jw = self.H_jw(
            zeros,
            poles
        )

        z = self.mag_H_jw(H_jw)
        z = np.clip(z, a_min=None, a_max=clip_limit)

        x = np.cos(w_plot)
        y = np.sin(w_plot)

        return x, y, z

    def tf2zpk(self, num, den):
        zeros, poles, gain = signal.tf2zpk(num, den)
        return zeros, poles, gain

    def dlti(self, zeros, poles, gain):
        list_poles = []
        for pair in poles.list:
            for p in pair:
                list_poles.append(p)

        list_zeros = []
        for pair in zeros.list:
            for z in pair:
                list_zeros.append(z)

        dlti = signal.dlti(list_zeros, list_poles, gain)
        return dlti

    def dimpulse(self, zeros, poles, gain=1):
        try:
            t, h = signal.dimpulse(self.sys_dlti, n=self.sample_size)
        except ValueError:  # bad system
            return [], []
        return t, h

    def dstep(self, zeros, poles):
        try:
            t, h = signal.dstep(self.sys_dlti, n=self.sample_size)
        except ValueError:  # bad system
            return [], []
        return t, h
