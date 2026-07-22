# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import matplotlib.patches as patches

from configs import *


decimals = 3
fontsize_arrow = 8
fontsize_block = 10
lw = 1.5

arrow_props = dict(
    arrowstyle="-|>",
    mutation_scale=15,
    color="black",
    lw=lw
)


class PlotterDiagram:
    def __init__(self, parent, app):
        self.app = app

        num, den = self.app.math_utils.H_z_inv_array(
            self.app.zeros,
            self.app.poles
        )
        list_num = list(num)
        list_den = list(den)

        if (not list_den[0].is_integer() or
            not int(list_den[0]) == 1        # TODO: when != 1
        ):
            print("invalid")
            return


        self.tl = tk.Toplevel(parent)
        self.tl.title("Diagrama de Blocos")

        self.tl.wait_visibility()
        self.tl.grab_set()


        n = len(list_num) - 1  # len(den) - 1


        list_den_minus = []
        for coef in den[1:]:
            list_den_minus.append(-coef)

        self.eq = self._y_n(list_num, list_den_minus, n)
        self.eq_generic = self._y_n_generic(n)


        # TODO: mv to SystemClassifier
        if (self.app.system_classifier.trivial or
            self.app.system_classifier.empty
        ):
            fir = True
        else:
            fir = True
            for coef in list_den[1:]:
                if not coef.is_integer() or int(coef) != 0:
                    fir = False
                    break

        x_lim = 10 if fir else 16
        y_lim = n*20/8 + 4


        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, x_lim)
        self.ax.set_ylim(0, y_lim)
        self.ax.axis("off")
        self.ax.set_title(
            self.eq_generic + "\n" + self.eq,
            loc="left",
            fontsize=10
        )

        self.diagram(n, fir)

        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tl)
        self.canvas.draw_idle()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.tl)
        self.toolbar.update()

    def _y_n(self, list_num, list_den_minus, n):
        expr_x = self._format_coefs_sym(list_num, "x", n)
        expr_y = self._format_coefs_sym(list_den_minus, "y", n)

        eq = "$" + f"y[n]={expr_x}{expr_y}" + "$"
        eq = eq.replace("=+", "=")
        return eq

    def _y_n_generic(self, n):
        eq = "$" + "y[n]=a_0 x[n]"
        for i in range(1, n+1):
            eq += f"+a_{i} x[n-{i}]"
        for i in range(1, n+1):
            eq += f"+b_{i} y[n-{i}]"
        eq += "$"
        return eq

    def _format_coefs_sym(self, list, sym, n):
        if len(list) == n + 1:
            offset_delay = 0
        else:
            offset_delay = 1
        print(offset_delay)
        print("n=", n)
        print("len(list)=", len(list))

        expr = ""
        for i, coef in enumerate(list):
            delay = i + offset_delay

            if coef.is_integer() and int(coef) == 0:
                continue

            if coef > 0:
                sign = "+"
            else:
                sign = ""

            if coef.is_integer() and int(coef) == 1:
                coef_str = f"{sign}"
            else:
                coef_str = f"{sign}{round(coef, decimals)}"

            if delay == 0:
                coef_str += f"{sym}[n]"
            else:
                coef_str += f"{sym}[n-{delay}]"

            expr += coef_str

        return expr

    def point(self, x, y):
        self.ax.plot(x, y, "ko", ms=5)

    def circle(self, x, y):
        circ = patches.Circle(
            (x, y),
            radius=0.4,
            facecolor=color_blocks,
            edgecolor="black",
            lw=lw
        )
        self.ax.add_patch(circ)
        self.ax.text(
            x,
            y,
            "+",
            fontsize=fontsize_block,
            ha="center",
            va="center"
        )

    def rectangle(self, x, y):
        rect = patches.Rectangle(
            (x, y),
            width=1.2,
            height=0.8,
            facecolor=color_blocks,
            edgecolor="black",
            lw=lw
        )
        self.ax.add_patch(rect)
        self.ax.text(
            x+0.6,
            y+0.4,
            "$z^{-1}$",
            fontsize=fontsize_block,
            ha="center",
            va="center"
        )

    def triangle(self, x, y, text, inv=False):
        h = 0.8
        dx_base = 0.2
        dx_tip = 0.6

        if not inv:
            x_base = x - dx_base
            x_tip  = x + dx_tip
        else:
            x_base = x + dx_base
            x_tip  = x - dx_tip

        tri = patches.Polygon(
            [[x_base, y+h/2], [x_base, y-h/2], [x_tip, y]],
            facecolor=color_blocks,
            edgecolor="black",
            lw=lw
        )
        self.ax.add_patch(tri)
        self.ax.text(
            x,
            y,
            text,
            fontsize=fontsize_block,
            ha="center",
            va="center"
        )

    def arrow_h(self, src, dst, text=""):
        self.ax.annotate("", xy=dst, xytext=src, arrowprops=arrow_props)

        if text:
            y_text = src[1] + 0.2
            x_text = src[0] + (dst[0]-src[0])/2
            self.ax.text(
                x_text,
                y_text,
                text,
                fontsize=fontsize_arrow,
                ha="center"
            )

    def arrow_down_90(self, src, dst):
        arrow_down = patches.FancyArrowPatch(
            src, dst,
            connectionstyle="angle,angleA=0,angleB=-90,rad=0",
            **arrow_props
        )
        self.ax.add_patch(arrow_down)

    def arrow_up_90(self, src, dst, text=""):
        arrow_return = patches.FancyArrowPatch(
            src, dst,
            connectionstyle="angle,angleA=0,angleB=90,rad=0",
            **arrow_props
        )
        self.ax.add_patch(arrow_return)

        if text:
            y_text = src[1] + 0.2
            x_text = src[0] + (dst[0]-src[0])/2
            self.ax.text(
                x_text,
                y_text,
                text,
                fontsize=fontsize_arrow,
                ha="center"
            )

    def diagram(self, n, fir):
        if fir:
            self.diagram_fir(n)
        else:
            self.diagram_l(n)
            self.diagram_r(n)

    def diagram_fir(self, n):
        self.diagram_part(n, text_start="x[n]", text_end="y[n]")

    def diagram_l(self, n):
        self.diagram_part(n, text_start="x[n]")

    def diagram_r(self, n):
        self.diagram_part(
            n,
            x_start=10,
            x_end=16,
            x_offset_rect=11,
            x_offset_circ=2.9,  # TODO: adapt + -> end
            x_offset_tri=7,
            inv=True,
            text_end="y[n]"
        )

    def diagram_part(
        self,
        n,
        x_start=0,
        x_end=10,
        x_offset_rect=0,
        x_offset_circ=0,
        x_offset_tri=0,
        inv=False,
        text_start="",
        text_end=""
    ):
        if inv:
            inv_mult = -1
            k = "b"
            var = "y"
        else:
            inv_mult = 1
            k = "a"
            var = "x"

        y_base = 1.9
        y_start = y_base*(n+1)

        x_tri = 4.7 + x_offset_tri
        x_tri_l = x_tri - 0.2*inv_mult
        x_tri_r = x_tri + 0.6*inv_mult

        r_circ = 0.4
        x_circ = 7 + x_offset_circ
        x_circ_l = x_circ - r_circ*inv_mult
        x_circ_r = x_circ + r_circ

        h_half_rect = 0.4
        len_half_rect = 0.6
        x_rect = 3 + x_offset_rect
        x_rect_l = x_rect - len_half_rect
        x_rect_r = x_rect + len_half_rect*inv_mult

        # Point
        if n > 1:
            self.point(x_rect, y_start)

        # Circle +
        self.circle(x_circ, y_start)

        # Triangle
        if inv_mult == 1:
            self.triangle(x_tri, y_start, text="$" + f"{k}_0" + "$")

            # Triangle -> +
            self.arrow_h(
                src=(x_tri_r, y_start),
                dst=(x_circ_l, y_start),
                text="$" + f"{k}_0{var}[n]" + "$"
            )

            # Point -> Triangle
            self.arrow_h(src=(x_rect, y_start), dst=(x_tri_l, y_start))

        # x|y [n] -> Point
        self.arrow_h(
            src=(x_start+0.5, y_start),
            dst=(x_rect, y_start),
            text=text_start
        )

        # + -> end
        self.arrow_h(
            src=(x_circ_r, y_start),
            dst=(x_end-0.5, y_start),
            text=text_end
        )

        for i in range(1, n+1):
            num = str(n-i+1)
            y_center = y_base*i

            # Rectangle -1
            self.rectangle(x_rect_l, y_center-h_half_rect)

            # Triangle
            self.triangle(
                x_tri,
                y_center,
                text="$" + f"{k}_{num}" + "$",
                inv=inv
            )

            # Point -> Rectangle -1
            self.arrow_down_90(
                src=(x_rect, y_center+y_base),
                dst=(x_rect, y_center+h_half_rect)
            )

            # Rectangle -1 -> Triangle
            self.arrow_h(
                src=(x_rect_r, y_center),
                dst=(x_tri_l, y_center),
                text=f"{var}[n-{num}]")

            # Rectangle -1 -> +
            self.arrow_up_90(
                src=(x_tri_r, y_center),
                dst=(x_circ, y_start-h_half_rect),
                text="$" + f"{k}_{num}{var}[n-{num}]" + "$"
            )
