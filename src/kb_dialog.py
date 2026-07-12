import math
import tkinter as tk

from configs import *


class KBDialog:
    def __init__(self, parent, app):
        self.app = app

        # Create Toplevel
        self.tl = tk.Toplevel(parent)
        self.tl.title("Inserção via Teclado")
        self.tl.resizable(True, True)

        # Keep the Toplevel in the front
        self.tl.transient(parent)
        self.tl.wait_visibility()  # wait until the win is drawn
        self.tl.grab_set()
        # self.tl.lift()

        # Add padding and color to the Toplevel
        self.tl.configure(bg=color_bg)

        self.dict_entries = {}
        self.dict_labels = {}

        # Main Frame
        fr = tk.Frame(self.tl, bg=color_bg, padx=10, pady=10)
        fr.pack(anchor="center", expand=True)


        # Pole/Zero Radiobuttons

        self.type_var = tk.StringVar(value="p")

        fr_type = tk.Frame(fr, bg=color_bg, pady=10)
        fr_type.grid(row=0, column=0, columnspan=2, sticky="ew")

        for bt in ["Polo", "Zero"]:
            rb = self._create_radiobutton(
                fr=fr_type,
                text=bt,
                variable=self.type_var,
                value=bt[0].lower(),
            )
            rb.pack(side="left", expand=True)


        # Rect/Polar Radiobuttons

        self.format_var = tk.StringVar(value="rect")
        fr_coord = tk.Frame(fr, bg=color_bg, pady=5)
        fr_coord.grid(row=1, column=0, columnspan=2, sticky="ew")

        self._create_radiobutton(
            fr=fr_coord,
            text="(X, Y)",
            variable=self.format_var,
            value="rect",
            command=self._update_label_texts,
        ).pack(side="left", expand=True)

        self._create_radiobutton(
            fr=fr_coord,
            text="(r, θ)",
            variable=self.format_var,
            value="polar",
            command=self._update_label_texts,
        ).pack(side="left", expand=True)


        # Entries
        for i in range(0, 2):
            label_entry = tk.Label(
                fr,
                text="X" if i == 0 else "Y",
                bg=color_bg,
                fg=color_text,
                anchor="w"
            )
            label_entry.grid(row=2+i, column=0, sticky="ew", pady=2)
            self.dict_labels[i] = label_entry

            entry = tk.Entry(fr, width=6)
            entry.grid(row=2+i, column=1, sticky="ew", padx=5, pady=2)

            entry.insert(0, "0")
            self.dict_entries[i] = entry

        # Buttons
        fr_bt = tk.Frame(self.tl, bg=color_bg, pady=10)
        fr_bt.pack(fill="x")

        for bt in [
            ("OK",     "left",  self._on_confirm),
            ("Cancel", "right", self._on_cancel)
        ]:
            tk.Button(
                fr_bt,
                text=bt[0],
                command=bt[2],
                width=10,
                relief="flat",
                overrelief="groove",
                cursor="hand2"
            ).pack(side=bt[1], padx=10, expand=True)

        self.app.center_toplevel(self.tl)

        # X click
        self.tl.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _create_radiobutton(self, fr, text, variable, value, command=None):
        bt = tk.Radiobutton(
            fr,
            text=text,
            variable=variable,
            value=value,
            command=command,
            bg=color_bg,
            fg=color_text,
            selectcolor=color_bg
        )
        return bt

    def _update_label_texts(self):
        if self.format_var.get() == "rect":
            self.dict_labels[0].config(text="X")
            self.dict_labels[1].config(text="Y")
        else:  # "rect"
            self.dict_labels[0].config(text="r")
            self.dict_labels[1].config(text="θ(°)")

    def _on_confirm(self):
        v0 = self.dict_entries[0].get()
        v1 = self.dict_entries[1].get()

        if isinstance(v0, str):
            v0 = v0.replace(",", ".")
        if isinstance(v1, str):
            v1 = v1.replace(",", ".")

        try:
            v0 = float(v0)
            v1 = float(v1)
        except ValueError:
            self.app.add_element_plane(None, None, None)
            return

        if self.format_var.get() == "polar":
            angle_rad = math.radians(v1)
            x = v0 * math.cos(angle_rad)
            y = v0 * math.sin(angle_rad)
        else:  # "rect"
            x = v0
            y = v1

        sel_type = self.type_var.get()

        if sel_type == "p":
            list_sel = self.app.list_poles
        else:  # "z"
            list_sel = self.app.list_zeros

        self.app.add_element_plane(list_sel, x, y)

    def _on_cancel(self):
        self.tl.destroy()
