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

        max_entries = 8
        self.list_entries_p = []
        self.list_entries_z = []

        self.list_labels_p = []
        self.list_labels_z = []

        fr_row_p = tk.Frame(fr_entries, bg=color_bg)
        fr_row_z = tk.Frame(fr_entries, bg=color_bg)

        fr_row_p.pack(side="top", fill="x", pady=2)
        fr_row_z.pack(side="top", fill="x", pady=2)

        for fr_row, list_entries, list_labels in (
            (fr_row_p, self.list_entries_p, self.list_labels_p),
            (fr_row_z, self.list_entries_z, self.list_labels_z)
        ):
            for i in range(0, max_entries+1):
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
                elif i == max_entries:
                    exp = dict_subst_exp[str(i)]
                    str_entry = f"z{exp_sign}{exp}"
                elif i == 1 and not self.app.var_z_inv.get():
                    str_entry = "z + "
                else:
                    exp = dict_subst_exp[str(i)]
                    str_entry = f"z{exp_sign}{exp} + "

                label = tk.Label(fr_row, text=str_entry, bg=color_bg)
                label.pack(side="left")

                list_labels.append(label)

        tk.Button(
            self.subfr_form,
            text="Calcular",
            command=self._on_calc,
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

    def show_entries(self):
        self.label_hz.pack_forget()
        self.subfr_form.pack()

        # Clear
        for list_entries in (self.list_entries_p, self.list_entries_z):
            for entry in list_entries:
                entry.delete(0, tk.END)
                entry.insert(0, "0")

    def show_labels(self):
        self.subfr_form.pack_forget()
        self.label_hz.pack()

    def update_labels(self):
        if self.app.var_z_inv.get():
            eq = self._format_H_z_inv(self.app.zeros, self.app.poles)
        else:
            eq = self._format_H_z(self.app.zeros, self.app.poles)

        self.label_hz.config(text=eq)

    def invert_z_entries(self):
        for list_labels in (self.list_labels_p, self.list_labels_z):
            for label in list_labels:
                current_text = label.cget("text")

                if self.app.var_z_inv.get():
                    if current_text == "z + ":
                        new_text = "z⁻¹ + "
                    else:
                        new_text = current_text.replace("z", "z⁻")
                else:
                    if current_text == "z⁻¹ + ":
                        new_text = "z + "
                    else:
                        new_text = current_text.replace("z⁻", "z")

                label.config(text=new_text)

    def _format_H_z_inv(self, zeros, poles):
        return self._format_H_z_eq(
            zeros,
            poles,
            self.app.math_utils.H_z_inv_eq,
            "⁻",
            "z_inv"
        )

    def _format_H_z(self, zeros, poles):
        return self._format_H_z_eq(
            zeros,
            poles,
            self.app.math_utils.H_z_eq,
            "",
            "z"
        )

    def _format_H_z_eq(self, zeros, poles, funct, sign, base):
        num, den = funct(zeros, poles)

        if num == 1 and den == 1:
            return "H(z) = 1"

        num = str(num)
        den = str(den)

        # Substitutions

        for exp in range(max_exp, 1, -1):
            new_exp = sign + "".join(dict_subst_exp[d] for d in str(exp))
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

    def _on_calc(self):
        num = []
        den = []
        for entry in self.list_entries_p:
            coef = entry.get().replace(",", ".")
            num.append(coef)
        for entry in self.list_entries_z:
            coef = entry.get().replace(",", ".")
            den.append(coef)

        num = [x if x.strip() != '' else '0' for x in num]
        den = [x if x.strip() != '' else '0' for x in den]

        try:
            num = [float(x) for x in num]
            den = [float(x) for x in den]

            if not any(x != 0.0 for x in den):
                valid = False
            else:
                valid = True
        except ValueError:
            valid = False

        if valid:
            if not self.app.var_z_inv.get():
                num.reverse()
                den.reverse()

            # Remove extra zeros in the end to reduce the polynomial degree
            while (
                len(num) > 1 and
                len(den) > 1 and
                num[-1] == 0.0 and
                den[-1] == 0.0
            ):
                num.pop()
                den.pop()

            zeros, poles, _ = self.app.math_utils.tf2zpk(num, den)

            self.app.clear_poles_zeros()

            for z in zeros:
                if z.imag >= 0:
                    self.app.add_element_plane(self.app.zeros, z.real, z.imag)
            for p in poles:
                if p.imag >= 0:
                    self.app.add_element_plane(self.app.poles, p.real, p.imag)

            self.app.update_all()
