import tkinter as tk
from tkinter import colorchooser

from configs import *


og_dict_colors = {
    "poles": color_poles,
    "zeros": color_zeros,
    "axes": color_axes,
    "bg_p": color_2d_bg,

    "curve": color_resp,
    # "axes": "#00ff00",
    "graduation": color_text,
    # "lines": "#0000ff",
    "grid": color_grid,
    "caption": color_text,
    "bg_r": color_2d_bg,
}

list_elements_p = [
    ("Polos", "poles"),
    ("Zeros", "zeros"),
    ("Eixos", "axes"),
    ("Fundo", "bg_p"),
]

list_elements_r = [
    ("Curva", "curve"),
    # ("Eixos", "axes"),
    ("Graduação", "graduation"),
    # ("Linhas de Cota", "lines"),
    ("Grades", "grid"),
    ("Legenda", "caption"),
    ("Fundo", "bg_r"),
]


class ColorDialog:
    def __init__(self, parent, app):
        self.app = app
        self.parent = parent

        self.dict_colors = og_dict_colors.copy()
        self.dict_bt = {}

    def open(self):
        self.tl = tk.Toplevel(self.parent)
        self.tl.title("Configuração de Cores")
        self.tl.transient(self.parent)

        self._create_buttons(
            title="Cores do Plano",
            list_elements=list_elements_p,
        )
        self._create_buttons(
            title="Cores do Gráfico",
            list_elements=list_elements_r,
        )

        fr_bottom = tk.Frame(self.tl, bg=color_bg, pady=10)
        fr_bottom.pack(fill="x")

        for bt in [
            ("Reset",  "left",  self._on_reset),
            ("Cancel", "right", self._on_cancel)
        ]:
            tk.Button(
                fr_bottom,
                text=bt[0],
                command=bt[2],
                width=10,
                relief="flat",
                overrelief="groove",
                cursor="hand2"
            ).pack(side=bt[1], padx=10, expand=True)

    def _create_buttons(self, title, list_elements):
        tk.Label(
            self.tl,
            text=title,
            font=("Arial", 10)
        ).pack(pady=15)

        fr_bt = tk.Frame(self.tl)
        fr_bt.pack(pady=5, padx=20, fill="both", expand=True)

        for name, key in list_elements:
            fr_row = tk.Frame(fr_bt)
            fr_row.pack(fill="x", pady=6)

            tk.Label(
                fr_row,
                text=name,
                width=18,
                anchor="w"
            ).pack(side="left")

            current_color = self.dict_colors[key]

            bt_color = tk.Button(
                fr_row,
                bg=current_color,
                width=6,
                relief="groove"
            )
            bt_color.config(
                command=lambda b=bt_color, k=key:
                self._open_selector(b, k)
            )
            bt_color.pack(side="right", padx=5)

            self.dict_bt[key] = bt_color

    def _open_selector(self, bt, key):
        color_hex = colorchooser.askcolor(
            initialcolor=bt["bg"],
            title="Selecione a Cor"
        )[1]

        if color_hex:
            bt.config(bg=color_hex)
            self.app.change_colors(key, color_hex)
            self.dict_colors[key] = color_hex

    def _on_reset(self):
        self.dict_colors = og_dict_colors.copy()
        for key, color in self.dict_colors.items():
            self.app.change_colors(key, color)

        for key, bt in self.dict_bt.items():
            bt.config(bg=self.dict_colors[key])

    def _on_cancel(self):
        self.tl.destroy()
