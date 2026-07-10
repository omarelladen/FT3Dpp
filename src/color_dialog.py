import tkinter as tk
from tkinter import colorchooser

from configs import *


# TODO: save default and current value
dict_colors = {
    "poles": color_poles,
    "zeros": color_zeros,
    "axes": color_axes,
    "bg_p": color_2d_bg,

    "curve": color_resp,
    # "axes": "#00ff00",
    "graduation": "black",
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

        self.tl = tk.Toplevel(parent)
        self.tl.title("Configuração de Cores")

        # self.tl.geometry("320x400")
        # self.tl.resizable(False, False)
        self.tl.transient(parent)
        # self.tl.grab_set()

        self._create_buttons(
            title="Cores do Plano",
            list_elements=list_elements_p,
        )
        self._create_buttons(
            title="Cores do Gráfico",
            list_elements=list_elements_r,
        )

    def _create_buttons(self, title, list_elements):
        tk.Label(
            self.tl,
            text=title,
            font=("Arial", 10)
        ).pack(pady=15)

        frame_bt = tk.Frame(self.tl)
        frame_bt.pack(pady=5, padx=20, fill="both", expand=True)

        for name, key in list_elements:
            row_frame = tk.Frame(frame_bt)
            row_frame.pack(fill="x", pady=6)

            tk.Label(
                row_frame,
                text=name,
                width=18,
                anchor="w"
            ).pack(side="left")

            current_color = dict_colors[key]

            bt_color = tk.Button(
                row_frame,
                bg=current_color,
                width=6,
                relief="groove"
            )
            bt_color.config(
                command=lambda b=bt_color, k=key:
                self._open_selector(b, k)
            )
            bt_color.pack(side="right", padx=5)

    def _open_selector(self, bt, key):
        color_hex = colorchooser.askcolor(
            initialcolor=bt["bg"],
            title="Selecione a Cor"
        )[1]

        if color_hex:
            bt.config(bg=color_hex)
            self.app.change_colors(key, color_hex)
            dict_colors[key] = color_hex
