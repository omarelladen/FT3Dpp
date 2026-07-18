# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)
from matplotlib import cm

from configs import *


class Plotter3D:
    def __init__(self, parent, app):
        self.app = app

        self.tl = tk.Toplevel(parent)
        self.tl.title("Gráfico 3D")

        self.tl.wait_visibility()
        self.tl.grab_set()

        # Blank Figure
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.view_init(elev=30, azim=45)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tl)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.tl)
        self.toolbar.update()


        self.init_resolution = 70
        self.max_resolution = 150

        self.init_clip = 10
        self.max_clip = 100

        self.app.math_utils.resolution_u = self.init_resolution
        self.app.math_utils.resolution_v = self.init_resolution
        self.app.math_utils.clip_limit_3d = self.init_clip

        self._update_curve()


        # Buttons

        self.fr_bt = tk.Frame(self.tl, bg=color_bg, pady=10)
        self.fr_bt.pack(fill="x")

        self.spin_res_v = self._create_spinbox(
            "Resolução V",
            cmd=self._change_resolution_v,
            from_=5,
            to=self.max_resolution,
            inc=5,
            init_value=self.init_resolution,
            unit="pts",
            side="right"
        )
        self.spin_res_u = self._create_spinbox(
            "Resolução U",
            cmd=self._change_resolution_u,
            from_=5,
            to=self.max_resolution,
            inc=5,
            init_value=self.init_resolution,
            unit="pts",
            side="right"
        )
        self.spin_clip = self._create_spinbox(
            "|H(z)|ₘₐₓ",
            cmd=self._change_clip,
            from_=1,
            to=self.max_clip,
            inc=1,
            init_value=self.init_clip,
            unit="",
            side="left"
        )

    def _create_spinbox(self, title, cmd, from_, to, inc, init_value, unit, side):
        fr_padx = 2

        label_unit = tk.Label(
            self.fr_bt,
            text=unit,
            fg=color_text,
            bg=color_bg
        )

        spin = tk.Spinbox(
            self.fr_bt,
            from_=from_, to=to,
            increment=inc,
            width=4,
            textvariable=tk.DoubleVar(value=init_value),
            bg=color_bg_spin,
            fg=color_text,
            insertbackground=color_text,
            buttonbackground=color_bg,
            command=cmd
        )

        label_title = tk.Label(
            self.fr_bt,
            text=f"{title} =",
            fg=color_text,
            bg=color_bg
        )

        if side == "right":
            label_unit.pack(side=side, padx=fr_padx)
            spin.pack(side=side, padx=fr_padx)
            label_title.pack(side=side, padx=(25, fr_padx))
        else:
            label_title.pack(side=side, padx=(25, fr_padx))
            spin.pack(side=side, padx=fr_padx)
            label_unit.pack(side=side, padx=fr_padx)

        # Events to confirm keyboard values
        spin.bind("<Return>",   lambda event: cmd())
        spin.bind("<FocusOut>", lambda event: cmd())

        return spin

    def _change_resolution_u(self):
        resolution = self.spin_res_u.get()
        if (resolution.isdigit() and
            int(resolution) > 1 and
            int(resolution) <= self.max_resolution
        ):
            self.app.math_utils.resolution_u = int(resolution)
            self._update_curve()
        else:
            self.spin_res_u.delete(0, "end")
            self.spin_res_u.insert(0, str(self.app.math_utils.resolution_u))

    def _change_resolution_v(self):
        resolution = self.spin_res_v.get()
        if (resolution.isdigit() and
            int(resolution) > 1 and
            int(resolution) <= self.max_resolution
        ):
            self.app.math_utils.resolution_v = int(resolution)
            self._update_curve()
        else:
            self.spin_res_v.delete(0, "end")
            self.spin_res_v.insert(0, str(self.app.math_utils.resolution_v))

    def _change_clip(self):
        clip = self.spin_clip.get()
        if (clip.isdigit() and
            int(clip) > 1 and
            int(clip) <= self.max_clip
        ):
            self.app.math_utils.clip_limit_3d = int(clip)
            self._update_curve()
        else:
            self.spin_res_v.delete(0, "end")
            self.spin_res_v.insert(0, str(self.app.math_utils.clip_limit_3d))

    def _update_curve(self):
        self.ax.clear()

        clip_limit = self.app.math_utils.clip_limit_3d

        self.ax.set_xlabel("Re")
        self.ax.set_ylabel("Im")
        self.ax.set_zlabel("|H(z)|")
        # self.ax.set_title("Gráfico 3D")
        self.ax.set_zlim(0, clip_limit)

        # Surface
        x_mesh, y_mesh, z_mesh = self.app.math_utils.mag_H_z_3D(
            self.app.zeros,
            self.app.poles,
            clip_limit
        )
        self.ax.plot_surface(
            x_mesh,
            y_mesh,
            z_mesh,
            cmap=cm.YlOrRd,
            linewidth=0.1,
            antialiased=True,
            edgecolor="gray",
            alpha=0.4
        )

        # Line in unit circle
        x_line, y_line, z_line = self.app.math_utils.mag_H_jw_3D(
            self.app.zeros,
            self.app.poles,
            clip_limit
        )
        self.ax.plot(
            x_line,
            y_line,
            z_line,
            color="blue",
            linewidth=3.5,
            label="|H(eʲʷ)|"
        )
        self.ax.legend()

        self.canvas.draw_idle()
