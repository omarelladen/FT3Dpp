import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)
from matplotlib import cm


class Plotter3D:
    def __init__(self, parent, app):
        self.app = app

        self.window = tk.Toplevel(parent)
        self.window.title("Gráfico 3D")
        self.window.transient(parent)

        # Blank Figure
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.view_init(elev=30, azim=45)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        self.toolbar.update()

        self._update_curve()

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
            self.app.list_zeros,
            self.app.list_poles,
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
            self.app.list_zeros,
            self.app.list_poles,
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
