# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import tkinter as tk

from configs import *


class TFDisplayer:
    def __init__(self, app, box):
        self.app = app

        self.subfr_form = tk.Frame(box, bg=color_bg)

        self.label_hz = self._create_label_fr_text(box, "H(z) = 1")

        self.lbl_form_text = self._create_label_fr_text(
            self.subfr_form,
            "H(z) = "
        )
        self.lbl_form_text.pack(side="left", padx=5)

        fr_entries = tk.Frame(self.subfr_form, bg=color_bg)
        fr_entries.pack(side="left", padx=5)

        max_tf_entries = 8
        self.list_tf_entries_p = []
        self.list_tf_entries_z = []

        self.list_tf_labels_p = []
        self.list_tf_labels_z = []

        fr_row_tf_p = tk.Frame(fr_entries, bg=color_bg)
        fr_row_tf_z = tk.Frame(fr_entries, bg=color_bg)

        fr_row_tf_p.pack(side="top", fill="x", pady=2)
        fr_row_tf_z.pack(side="top", fill="x", pady=2)

        for fr_row, list_entries, list_labels in (
            (fr_row_tf_p, self.list_tf_entries_p, self.list_tf_labels_p),
            (fr_row_tf_z, self.list_tf_entries_z, self.list_tf_labels_z)
        ):
            for i in range(0, max_tf_entries+1):
                entry = tk.Entry(fr_row, width=5)
                entry.pack(side="left")
                entry.insert(0, "0")
                list_entries.append(entry)

                if self.app.var_z_inv.get():
                    exp_sign = "⁻"
                else:
                    exp_sign = ""

                if i == 0:
                    str_entry = " + "
                elif i == max_tf_entries:
                    exp = dict_subst_exp[str(i)]
                    str_entry = f"z{exp_sign}{exp}"
                else:
                    exp = dict_subst_exp[str(i)]
                    str_entry = f"z{exp_sign}{exp} + "

                label = tk.Label(fr_row, text=str_entry, bg=color_bg)
                label.pack(side="left")

                list_labels.append(label)

        tk.Button(
            self.subfr_form,
            text="Calcular",
            command=self._on_calc_tf2zpk,
            # width=10,
            relief="flat",
            overrelief="groove",
            cursor="hand2"
        ).pack(side="left", padx=5)

    def _create_label_fr_text(self, master, text):
        label = tk.Label(
            master,
            text=text,
            fg=color_text,
            bg=color_bg,
            font=("Consolas", 11)
        )
        label.pack(expand=True)
        return label

    def show_tf_entries(self):
        self.label_hz.pack_forget()
        self.subfr_form.pack()

        # Clear
        # for entry in self.list_tf_entries_p:
        #     entry.delete(0, tk.END)
        #     entry.insert(0, "0")

    def update_label_tf(self):
        if self.app.var_z_inv.get():
            eq = self.app.math_utils.format_H_z_inv(self.app.zeros, self.app.poles)
        else:
            eq = self.app.math_utils.format_H_z(self.app.zeros, self.app.poles)
        self.subfr_form.pack_forget()
        self.label_hz.config(text=eq)
        self.label_hz.pack()

    def update_entries_tf(self):
        for list_labels in (self.list_tf_labels_p, self.list_tf_labels_z):
            for label in list_labels:
                current_text = label.cget("text")
                if self.app.var_z_inv.get():
                    new_text = current_text.replace("z", "z⁻")
                else:
                    new_text = current_text.replace("z⁻", "z")
                label.config(text=new_text)

    def _on_calc_tf2zpk(self):
        pass
