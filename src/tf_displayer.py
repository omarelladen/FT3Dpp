# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import tkinter as tk

from configs import *


max_exp = 20

dict_subst_z = {
    "z_inv": "z⁻¹",
    "*": "",
    "1.0z": "z",
    "z⁻¹ + 1.0": "z⁻¹ + 1",
    " ": ""
}

dict_subst_exp = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
}


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
            eq = self._format_H_z_inv(self.app.zeros, self.app.poles)
        else:
            eq = self._format_H_z(self.app.zeros, self.app.poles)
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

    def _format_H_z_inv(self, zeros, poles):
        return self._format_H_z_eq(
            zeros,
            poles,
            self.app.math_utils.calc_H_z_inv_eq,
            "⁻",
            "z_inv"
        )

    def _format_H_z(self, zeros, poles):
        return self._format_H_z_eq(
            zeros,
            poles,
            self.app.math_utils.calc_H_z_eq,
            "",
            "z"
        )

    def _format_H_z_eq(self, zeros, poles, funct, signal, base):
        num, den = funct(zeros, poles)

        if num == 1 and den == 1:
            return "H(z) = 1"

        num = str(num)
        den = str(den)

        # Substitutions

        for exp in range(max_exp, 1, -1):
            new_exp = signal + "".join(dict_subst_exp[d] for d in str(exp))
            num = num.replace(f"{base}**{exp}", f"z{new_exp}")
            den = den.replace(f"{base}**{exp}", f"z{new_exp}")

        for old, new in dict_subst_z.items():
            num = num.replace(old, new)
            den = den.replace(old, new)

        return self._create_eq(num, den)

    def _create_eq(self, num, den):
        bar_size = max(len(num), len(den))
        bar = "—" * bar_size

        num_center = num.center(bar_size)
        den_center = den.center(bar_size)

        return (
            f"       {num_center}\n"
            f"H(z) = {bar}\n"
            f"       {den_center}"
        )
