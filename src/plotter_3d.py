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
        self.tl.transient(parent)

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
        self.app.math_utils.resolution_u = self.init_resolution
        self.app.math_utils.resolution_v = self.init_resolution

        self._update_curve()


        # Buttons

        self.fr_bt = tk.Frame(self.tl, bg=color_bg, pady=10)
        self.fr_bt.pack(fill="x")

        self.box_res_v = self._create_spinbox("V", self._change_resolution_v)
        self.box_res_u = self._create_spinbox("U", self._change_resolution_u)

    def _create_spinbox(self, axis, cmd):
        fr_padx = 2

        tk.Label(
            self.fr_bt,
            text="pts",
            fg=color_text,
            bg=color_bg
        ).pack(side="right", padx=fr_padx)

        spinbox = tk.Spinbox(
            self.fr_bt,
            from_=5, to=self.max_resolution,
            increment=5,
            width=4,
            textvariable=tk.DoubleVar(value=self.init_resolution),
            bg=color_bg_spin,
            fg=color_text,
            insertbackground=color_text,
            buttonbackground=color_bg,
            command=cmd
        )
        spinbox.pack(side="right", padx=fr_padx)

        tk.Label(
            self.fr_bt,
            text=f"Resolução {axis} =",
            fg=color_text,
            bg=color_bg
        ).pack(side="right", padx=(25, fr_padx))

        # Events to confirm keyboard values
        spinbox.bind("<Return>",   lambda event: cmd())
        spinbox.bind("<FocusOut>", lambda event: cmd())

        return spinbox

    def _change_resolution_u(self):
        resolution = self.box_res_u.get()
        if (resolution.isdigit() and
            int(resolution) > 1 and
            int(resolution) <= self.max_resolution
        ):
            self.app.math_utils.resolution_u = int(self.box_res_u.get())
            self._update_curve()
        else:
            self.box_res_u.delete(0, "end")
            self.box_res_u.insert(0, str(self.app.math_utils.resolution_u))

    def _change_resolution_v(self):
        resolution = self.box_res_v.get()
        if (resolution.isdigit() and
            int(resolution) > 1 and
            int(resolution) <= self.max_resolution
        ):
            self.app.math_utils.resolution_v = int(self.box_res_v.get())
            self._update_curve()
        else:
            self.box_res_v.delete(0, "end")
            self.box_res_v.insert(0, str(self.app.math_utils.resolution_v))

    def _update_curve(self):
        self.ax.clear()

        clip_limit = 10

        self.ax.set_xlabel("Re")
        self.ax.set_ylabel("Im")
        self.ax.set_zlabel("|H(z)|")
        # self.ax.set_title("Gráfico 3D")
        self.ax.set_zlim(0, clip_limit)

        # Surface
        x_mesh, y_mesh, z_mesh = self.app.math_utils.calc_mag_H_3D(
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
        x_line, y_line, z_line = self.app.math_utils.calc_line_3D(
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
