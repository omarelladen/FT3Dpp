import tkinter as tk

from configs import *


class KBMenu:
    def __init__(self, parent, app):
        self.app = app

        # Create Toplevel
        self.tl = tk.Toplevel(parent)
        self.tl.title("Inserção de Polos e Zeros via Teclado")
        self.tl.resizable(False, False)

        # Keep the Toplevel in the front
        self.tl.transient(parent)
        self.tl.wait_visibility()  # wait until the win is drawn
        self.tl.grab_set()
        # self.tl.lift()

        # Add padding and color to the Toplevel
        self.tl.configure(bg=color_bg)

        self.entries = {}

        # Frame
        fr = tk.Frame(self.tl, bg=color_bg, padx=10, pady=10)
        fr.pack(anchor="center", expand=True)


        # Pole/Zero Radiobuttons

        self.mode_var = tk.StringVar(value="p")

        fr_type = tk.Frame(fr, bg=color_bg, pady=10)
        fr_type.grid(row=0, column=0, columnspan=2, sticky="ew")

        for bt in ["Polo", "Zero"]:
            rb = tk.Radiobutton(
                fr_type,
                text=bt,
                variable=self.mode_var,
                value=bt[0].lower(),
                bg=color_bg,
                fg=color_text,
                selectcolor=color_bg,
                activebackground=color_bg,
                activeforeground=color_text
            )
            rb.pack(side="left", expand=True)

        # Axes values
        for i, axis in enumerate(["X", "Y"]):
            tk.Label(
                fr,
                text=axis,
                bg=color_bg,
                fg=color_text,
                anchor="w"
            ).grid(row=1+i, column=0, sticky="ew", pady=2)

            entry = tk.Entry(fr, width=6)
            entry.grid(row=1+i, column=1, sticky="ew", padx=5, pady=2)

            entry.insert(0, "0")
            self.entries[axis] = entry

        # Buttons
        bt_fr = tk.Frame(self.tl, bg=color_bg, pady=10)
        bt_fr.pack(fill="x")

        for bt in [("Cancel", "left", self.on_cancel), ("OK", "right", self.on_confirm)]:
            tk.Button(
                bt_fr,
                text=bt[0],
                command=bt[2],
                width=10,
                relief="flat",
                overrelief="groove",
                cursor="hand2"
            ).pack(side=bt[1], padx=10, expand=True)

        self.app.center_toplevel(self.tl)

        # X click
        self.tl.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def on_confirm(self):
        updates = {}
        for v_name, widget_item in self.entries.items():
            updates[v_name] = widget_item.get()

        self.tl.destroy()

        sel_type = self.mode_var.get()
        if sel_type == "p":
            sel_list = self.app.list_poles
        else:  # "z":
            sel_list = self.app.list_zeros

        self.app.add_element_plane(sel_list, updates["X"], updates["Y"])
        self.app.update_plane()
        self.app.update_freq_resp()

    def on_cancel(self):
        self.tl.destroy()
