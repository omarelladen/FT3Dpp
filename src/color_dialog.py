import tkinter as tk
from tkinter import colorchooser


# TODO: save default and current value
dict_color_menu = {
    "curve": "#ffffff",
    "axes": "#00ff00",
    "graduation": "#ffff00",
    "lines": "#0000ff",
    "grid": "#008000",
    "caption": "#ffffff",
    "bg": "#000000",
}

list_elements = [
    ("Curva", "curve"),
    ("Eixos", "axes"),
    ("Graduação", "graduation"),
    ("Linhas de Cota", "lines"),
    ("Grades", "grid"),
    ("Legenda", "caption"),
    ("Fundo", "bg"),
]


class ColorDialog:
    def __init__(self, parent, app):
        self.app = app

        tl = tk.Toplevel(parent)
        tl.title("Configuração de Cores")

        # tl.geometry("320x400")
        tl.resizable(False, False)
        tl.transient(parent)
        # tl.grab_set()

        tk.Label(
            tl,
            text="Cores do Gráfico",
            font=("Arial", 10)
        ).pack(pady=15)

        frame_bt = tk.Frame(tl)
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

            current_color = dict_color_menu[key]

            bt_color = tk.Button(
                row_frame,
                bg=current_color,
                width=6,
                relief="groove"
            )
            bt_color.config(
                command=lambda b=bt_color, k=key:
                self.open_selector(b, k)
            )
            bt_color.pack(side="right", padx=5)

    def open_selector(self, botao, key):
        cor_hex = colorchooser.askcolor(
            initialcolor=botao["bg"],
            title="Selecione a Cor"
        )[1]

        if cor_hex:
            botao.config(bg=cor_hex)
            self.app.update_colors(key, cor_hex)
            dict_color_menu[key] = cor_hex
