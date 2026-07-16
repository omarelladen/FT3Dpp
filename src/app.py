# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import os
import tkinter as tk
from tkinter import messagebox

import numpy as np

import matplotlib.patches as patches
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from configs import *

from math_utils import MathUtils
from color_dialog import ColorDialog
from kb_dialog import KBDialog
from about_dialog import AboutDialog
from help_dialog import HelpDialog
from plotter_3d import Plotter3D
from elements import Elements
from tf_displayer import TFDisplayer
from system_classifier import SystemClassifier


icon_logo_path = os.path.join("icons", "logo.png")

range_click = 0.1

max_pi = 4

init_resolution = 500
max_resolution = 1000

dpi = 100

ax_text_pos = 1.6
lim_plane = 1.3
lw = 1.5
win_size = "1000x620"

R_BUTTON = 3
L_BUTTON = 1


class App:
    def __init__(self):
        self.math_utils = MathUtils(init_resolution, max_pi)

        # Main Window
        self.win = tk.Tk()
        self.win.title(app_name)
        self.win.geometry(win_size)
        self.win.configure(bg=color_bg)

        # Icon
        if os.name == "nt":  # Windows
            if os.path.isfile(icon_logo_path):
                try:
                    self.win.iconphoto(
                        True,
                        tk.PhotoImage(file=icon_logo_path)
                    )
                except Exception as e:
                    print(f"Error loading icon {icon_logo_path}: {e}")


        # Menu Bar

        small_font = ("Arial", 8)
        self.menubar = tk.Menu(self.win, font=small_font)


        # self.menu_file     = self._create_menu()
        # self.menu_edit     = self._create_menu()
        # self.menu_entry    = self._create_menu()
        # self.menu_plane    = self._create_menu()
        self.menu_system   = self._create_menu()
        # self.menu_graphics = self._create_menu()
        self.menu_colors   = self._create_menu()
        # self.menu_windows  = self._create_menu()
        self.menu_help     = self._create_menu()

        self.menu_colors.add_command(label="Cores", command=self._open_color_dialog)

        self.menu_help.add_command(label="Ajuda", command=self._open_help_dialog)
        self.menu_help.add_command(label="Sobre", command=self._open_about_dialog)


        # self.menubar.add_cascade(label="Arquivo", menu=self.menu_file)
        # self.menubar.add_cascade(label="Editar", menu=self.menu_edit)
        # self.menubar.add_cascade(label="Entrada de Raízes", menu=self.menu_entry)
        # self.menubar.add_cascade(label="Plano", menu=self.menu_plane)
        self.menubar.add_cascade(label="Sistema", menu=self.menu_system)
        self.menubar.add_cascade(label="Cores", menu=self.menu_colors)
        # self.menubar.add_cascade(label="Gráficos", menu=self.menu_graphics)
        # self.menubar.add_cascade(label="Janelas", menu=self.menu_windows)
        self.menubar.add_cascade(label="Ajuda", menu=self.menu_help)


        # Show Menu Bar
        self.win.config(menu=self.menubar)

        self.toolbar = tk.Frame(self.win, bd=1, relief="raised", bg=color_bg)


        # Icons

        self.icon_open = self._create_icon("open_t.png")
        self.icon_save = self._create_icon("save_t.png")
        self.icon_plane = self._create_icon("plane_t.png")
        self.icon_plane_top = self._create_icon("plane_top_t.png")
        self.icon_freq = self._create_icon("freq_t.png", 16)
        self.icon_freq_db = self._create_icon("freq_db_t.png", 16)
        self.icon_phase = self._create_icon("phase_t.png", 16)
        self.icon_imp = self._create_icon("imp_t.png", 16)
        self.icon_deg = self._create_icon("deg_t.png", 16)
        self.icon_3d = self._create_icon("3d_t.png", 16)

        self.icon_pole = self._create_icon("pole.png", 3)
        self.icon_zero = self._create_icon("zero.png", 3)
        self.icon_kb = self._create_icon("kb.png", 3)
        # self.icon_zoom = self._create_icon("zoom.png", 3)
        # self.icon_hand = self._create_icon("hand.png", 3)
        # self.icon_dim = self._create_icon("dim.png", 3)
        self.icon_clear = self._create_icon("clear.png", 3)
        self.icon_info = self._create_icon("info.png", 3)

        # self.icon_exit = self._create_icon("exit.png", 6)
        # self.icon_graphic = self._create_icon("graphic.png", 6)
        # self.icon_save_as = self._create_icon("save_as.png", 6)

        # Buttons
        self.dict_bt = {
            self.icon_open: ("Abrir Arquivo", -1, False),
            self.icon_save: ("Salvar Arquivo", -1, False),
            self.icon_plane: ("Entrada via Plano Complexo", 0, True),
            "FT": ("Entrada via Função de Transferência", 0, False),
            self.icon_plane_top: ("Topografia do Plano", -1, False),
            "S": ("Plano s", 1, False),
            "Z": ("Plano z", 1, True),
            self.icon_freq: ("Magnitude", 2, True),
            self.icon_freq_db: ("Magnitude (dB)", 2, False),
            self.icon_phase: ("Fase", 2, False),
            self.icon_imp: ("Resposta ao Impulso", -1, False),
            self.icon_deg: ("Resposta ao Degrau Unitário", -1, False),
            self.icon_3d: ("Gráfico 3D", -1, False),

            self.icon_pole: ("Editar Polos", 3, True),
            self.icon_zero: ("Editar Zeros", 3, False),
            self.icon_kb: ("Inserir Raízes via Teclado", -1, False),
            # self.icon_zoom: ("Zoom no Plano", -1, False),
            # self.icon_hand: ("Movimentar o Plano", -1, False),
            # self.icon_dim: ("Restaurar Dimensões do Plano", -1, False),
            self.icon_clear: ("Limpar", -1, False),
            self.icon_info: ("Maiores Informações", -1, False),

            # self.icon_exit: ("Sair", -1, False),
            # self.icon_graphic: ("Salvar Gráfico", -1, False),
            # self.icon_save_as: ("Salvar como", -1, False),
        }

        self.bt_states = {}
        self.bt_groups = {}

        # Top Buttons
        self._create_bts(list(self.dict_bt.items())[:13], "top")
        self.toolbar.pack(side="top", fill="x")

        self.fr_top = tk.Frame(self.win, bg=color_bg, pady=5)
        self.fr_top.pack(side="top", fill="x", padx=10)

        self.main_container = tk.Frame(self.win, bg=color_bg)
        self.main_container.pack(
            side="top",
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=5
        )

        # Left Buttons
        self.fr_bt_left = tk.Frame(self.main_container, bg=color_bg)
        self.fr_bt_left.pack(side="left", fill="y", padx=5, pady=5)
        self._create_bts(list(self.dict_bt.items())[13:], "left")


        # Poles and zeros

        self.poles = Elements("p")
        self.zeros = Elements("z")

        box_poles = self._create_label_fr(self.fr_top, "Polos")
        box_zeros = self._create_label_fr(self.fr_top, "Zeros")

        fr_poles_outer, self.fr_poles = self._create_scrollable_fr(
            box_poles,
            width=200,
            height=45,
            bg_color=color_bg
        )
        fr_poles_outer.pack(side="left", padx=5, pady=5)

        fr_zeros_outer, self.fr_zeros = self._create_scrollable_fr(
            box_zeros,
            width=200,
            height=45,
            bg_color=color_bg
        )
        fr_zeros_outer.pack(side="left", padx=5, pady=5)

        self.text_poles_var = tk.StringVar()
        self.text_zeros_var = tk.StringVar()

        self._create_label_coords(self.fr_poles, self.text_poles_var)
        self._create_label_coords(self.fr_zeros, self.text_zeros_var)


        self.box_stats = self._create_label_fr(
            self.fr_top,
            "Total"
        )
        self.label_stats = tk.Label(
            self.box_stats,
            text="",
            fg=color_text,
            bg=color_bg
        )
        self.label_stats.grid(row=0, column=0, padx=2, pady=2)

#         self.fr_limits = self._create_label_fr(
#             self.fr_top,
#             "Limites do Plano"
#         )
#         self.spin_a = self._create_spin_top(0, 1, 0, "Eixo X")
#         self.spin_b = self._create_spin_top(0, 3, 2, "a")
#         self.spin_c = self._create_spin_top(1, 1, 0, "Eixo Y")
#         self.spin_d = self._create_spin_top(1, 3, 2, "a")


#         entry = tk.Entry(
#             self.fr_bottom,
#             width=20,
#             bg="#151515",
#             fg="white",
#             insertbackground="white"
#         )
#         color_text.pack(side="left")


        # Bottom Frame

        self.fr_bottom = tk.Frame(self.win, bg=color_bg, pady=4)
        self.fr_bottom.pack(side="bottom", fill="x", padx=10)

        # z inv checkbox
        self.var_z_inv = tk.BooleanVar(value=True)
        self.check_z_inv = tk.Checkbutton(
            self.fr_bottom,
            text="z⁻ⁿ",
            variable=self.var_z_inv,
            bg=color_bg,
            fg=color_text,
            selectcolor=color_bg_spin,
            activebackground=color_bg,
            activeforeground=color_text,
            command=self._on_z_inv_click
        )
        self.check_z_inv.pack(side="left", padx=10)


        # Transfer Function equation
        box_tf = self._create_label_fr(
            self.fr_bottom,
            "Função de Transferência"
        )
        self.tf_displayer = TFDisplayer(self, box_tf)

        # Figure Frames
        self.fr_plane = self._create_fr_fig(width=360)
        self.fr_resp  = self._create_fr_fig(width=600)


        # Plane Figure

        self.fig_p = Figure(figsize=(2.8, 2.8), dpi=dpi, facecolor=color_bg)
        self.ax_p = self.fig_p.add_subplot()
        self.ax_p.set_facecolor(color_2d_bg)
        self.ax_p.set_xlim(-lim_plane, lim_plane)
        self.ax_p.set_ylim(-lim_plane, lim_plane)
        self.ax_p.set_aspect("equal")
        self.ax_p.set_title(
            "Plano z",
            color=color_text,
            fontsize=10,
            pad=10,
            loc="left"
        )

        # Axes
        self.ax_p.text(
            0.5, 1.02,
            "Im",
            color=color_text,
            fontsize=8,
            fontweight="bold",
            ha="center",
            va="bottom",
            transform=self.ax_p.transAxes
        )
        self.ax_p.text(
            1.02, 0.5,
            "Re",
            color=color_text,
            fontsize=8,
            fontweight="bold",
            ha="left",
            va="center",
            transform=self.ax_p.transAxes
        )

        # Circle
        self.ln_ax_p_h = self.ax_p.axhline(0, color=color_axes, lw=lw, zorder=1)
        self.ln_ax_p_v = self.ax_p.axvline(0, color=color_axes, lw=lw, zorder=1)
        self.circle = patches.Circle(
            xy=(0, 0),
            radius=1,
            color=color_axes,
            fill=False,
            lw=lw,
            zorder=1
        )
        self.ax_p.add_patch(self.circle)

        self.points_plot_poles = self._setup_point_plotter("x", color_poles)
        self.points_plot_zeros = self._setup_point_plotter("o", color_zeros)

        self.idx_sel_point = None

        self.canvas_p = FigureCanvasTkAgg(self.fig_p, master=self.fr_plane)
        self.canvas_p.draw()

        # Matplotlib toolbar
        self.toolbar_p = NavigationToolbar2Tk(
            self.canvas_p,
            window=self.fr_plane,
            pack_toolbar=False
        )
        self.toolbar_p.update()

        self.canvas_p.get_tk_widget().pack(
            side="top",
            fill=tk.NONE,
            expand=False,
            pady=(2, 0)
        )
        self.toolbar_p.pack(side="top", fill=tk.X)

        # System classification
        self.label_system = tk.Label(
            self.fr_plane,
            text="",
            fg="white",
            bg=color_bg,
            font=("Arial", 10),
            anchor="w",
            pady=10
        )
        self.label_system.pack(side="top", fill="x", padx=10)

        # Plane Events
        self.fig_p.canvas.mpl_connect("button_press_event",   self._on_click)
        self.fig_p.canvas.mpl_connect("motion_notify_event",  self._on_move)
        self.fig_p.canvas.mpl_connect("button_release_event", self._on_drop)


        # Frequency Response Figure

        self.fig_r = Figure(figsize=(10, 2.8), dpi=dpi, facecolor=color_bg)
        self.ax_r = self.fig_r.add_subplot()
        self.ax_r.set_facecolor(color_2d_bg)
        self.ax_r.grid(True, color=color_grid, linestyle="--")
        self.ax_r.tick_params(colors=color_text)
        self.ax_r.set_ylim(-1, 1)
        self._set_freq_resp_title("Resposta em Frequência: Magnitude")

        self.line_r, = self.ax_r.plot([], [], color=color_resp, linewidth=2)

        # Set x ticks as multiples of pi
        step = 0.5*np.pi
        intervals = np.arange(0, max_pi*np.pi + step, step)
        self.ax_r.set_xticks(intervals)

        # Format x axis label

        def formatter_pi(v, pos):
            mult = round(v / np.pi, 2)
            if mult == 0:
                return "0"
            if mult == 1:
                return "π"
            if mult.is_integer():
                return f"{int(mult)}π"
            return f"{mult}π"

        self.ax_r.xaxis.set_major_formatter(ticker.FuncFormatter(formatter_pi))
        self.ax_r.format_coord = lambda x, y: f"(x, y) = ({x:.2f}, {y:.2f})"

        self.canvas_r = FigureCanvasTkAgg(self.fig_r, master=self.fr_resp)
        self.canvas_r.draw()

        # Matplotlib toolbar
        self.toolbar_r = NavigationToolbar2Tk(
            self.canvas_r,
            window=self.fr_resp,
            pack_toolbar=False
        )
        self.toolbar_r.update()

        self.canvas_r.get_tk_widget().pack(
            side="top",
            fill=tk.NONE,
            expand=False,
            pady=(2, 0)
        )
        self.toolbar_r.pack(side="top", fill=tk.X)


        # Frquency response bottom Frame

        self.fr_input_r = tk.Frame(self.fr_resp, bg=color_bg, pady=5)
        self.fr_input_r.pack(side="top", fill="x")

        fr_r_padx = 2

        # Theta Spin

        tk.Label(
            self.fr_input_r,
            text="θₘₐₓ =",
            fg=color_text,
            bg=color_bg
        ).pack(side="left", padx=fr_r_padx)

        self.theta_max = tk.Spinbox(
            self.fr_input_r,
            from_=1, to=max_pi,
            increment=1,
            width=2,
            state="readonly",  # block kb
            bg=color_bg_spin,
            fg=color_text,
            insertbackground=color_text,
            buttonbackground=color_bg,
            command=self.update_freq_resp
        )
        self.theta_max.pack(side="left", padx=fr_r_padx)

        tk.Label(
            self.fr_input_r,
            text="π",
            fg=color_text,
            bg=color_bg
        ).pack(side="left", padx=fr_r_padx)

        # Normalized checkbox
        self.var_normalize = tk.BooleanVar(value=True)
        self.check_normalize = tk.Checkbutton(
            self.fr_input_r,
            text="Normalizado",
            variable=self.var_normalize,
            bg=color_bg,
            fg=color_text,
            selectcolor=color_bg_spin,
            activebackground=color_bg,
            activeforeground=color_text,
            command=self.update_freq_resp
        )
        self.check_normalize.pack(side="left", padx=10)

        # Phase unit checkbox
        self.var_phase_deg = tk.BooleanVar(value=True)
        self.check_phase_unit = tk.Checkbutton(
            self.fr_input_r,
            text="Graus",
            variable=self.var_phase_deg,
            bg=color_bg,
            fg=color_text,
            selectcolor=color_bg_spin,
            activebackground=color_bg,
            activeforeground=color_text,
            command=self.update_freq_resp
        )


        # Resolution Spin

        tk.Label(
            self.fr_input_r,
            text="pts (0-π)",
            fg=color_text,
            bg=color_bg
        ).pack(side="right", padx=fr_r_padx)

        self.resolution = tk.Spinbox(
            self.fr_input_r,
            from_=5, to=max_resolution,
            increment=5,
            width=4,
            textvariable=tk.DoubleVar(value=init_resolution),
            bg=color_bg_spin,
            fg=color_text,
            insertbackground=color_text,
            buttonbackground=color_bg,
            command=self._change_resolution
        )
        self.resolution.pack(side="right", padx=fr_r_padx)

        tk.Label(
            self.fr_input_r,
            text="Resolução =",
            fg=color_text,
            bg=color_bg
        ).pack(side="right", padx=fr_r_padx)


        self.color_dialog = ColorDialog(self.win, self)
        self.system_classifier = SystemClassifier(self)

        # Events to confirm keyboard values
        self.resolution.bind("<Return>",   lambda event: self._change_resolution())
        self.resolution.bind("<FocusOut>", lambda event: self._change_resolution())

        self.update_all()

    def _create_icon(self, filename, reduction=18):
        file_path = os.path.join("icons", filename)
        if os.path.isfile(file_path):
            try:
                img = tk.PhotoImage(file=file_path)
                img = img.subsample(reduction, reduction)
                return img
            except Exception as e:
                print(f"Error loading image '{file_path}': {e}")

    def change_colors(self, key, new_color):
        if key == "poles":
            self.points_plot_poles.set_color(new_color)
        elif key == "zeros":
            self.points_plot_zeros.set_color(new_color)
        elif key == "axes":
            self.ln_ax_p_h.set_color(new_color)
            self.ln_ax_p_v.set_color(new_color)
            self.circle.set_edgecolor(new_color)
        elif key == "bg_p":
            # self.fig_p.patch.set_facecolor(new_color)
            self.ax_p.set_facecolor(new_color)
        elif key == "curve":
            self.line_r.set_color(new_color)
        elif key == "graduation":
            self.ax_r.tick_params(color=new_color)
        elif key == "grid":
            self.ax_r.grid(True, color=new_color)
        elif key == "bg_r":
            # self.fig_r.patch.set_facecolor(new_color)
            self.ax_r.set_facecolor(new_color)
        elif key == "caption":
            self.ax_r.tick_params(labelcolor=new_color)

        self.canvas_p.draw_idle()
        self.canvas_r.draw_idle()

    def _open_kb_dialog(self):
        KBDialog(self.win, self)

    def _open_color_dialog(self):
        self.color_dialog.open()

    def _open_about_dialog(self):
        AboutDialog(self.win, self)

    def _open_help_dialog(self):
        HelpDialog(self.win, self)

    def _open_sys_clf_info(self):
        msg = self.system_classifier.info()
        self._show_info(
            title="Informações adicionais sobre o sistema",
            msg=msg
        )

    def _show_info(self, msg, title="Info"):
        messagebox.showinfo(title=title, message=msg)

    def _show_warning(self, msg, title="Aviso"):
        messagebox.showwarning(title=title, message=msg)

    def _show_error(self, msg, title="Erro"):
        messagebox.showerror(title=title, message=msg)

    def add_element_plane(self, list_sel, x, y):
        '''Called only once for each complex conjugate pair'''
        if list_sel is None:
            self._show_error("Valor Inválido")
            return

        list_sel.add(x, y)

    def _change_resolution(self):
        resolution = self.resolution.get()
        if (resolution.isdigit() and
            int(resolution) > 1 and
            int(resolution) <= max_resolution
        ):
            self.math_utils.resolution = int(self.resolution.get())
            self.update_freq_resp()
        else:
            self.resolution.delete(0, "end")
            self.resolution.insert(0, str(self.math_utils.resolution))

    def update_freq_resp(self):
        theta_val = int(self.theta_max.get())
        self.math_utils.max_pi = theta_val

        w_plot = self.math_utils.get_w_plot()
        H_z = self.math_utils.H(self.zeros, self.poles)

        # Select what to plot
        if self.bt_states[self.icon_phase].get():
            if self.var_phase_deg.get():
                ang_H = self.math_utils.phase_H_deg(H_z)
                self._set_freq_resp_title("Resposta em Frequência: Fase (graus)")
            else:
                ang_H = self.math_utils.phase_H_rad(H_z)
                self._set_freq_resp_title("Resposta em Frequência: Fase (rad)")
            line = ang_H
            self._set_phase_checkbox()
        elif self.bt_states[self.icon_freq_db].get():
            if self.var_normalize.get():
                mag_H_db = self.math_utils.mag_H_db_norm(H_z)
            else:
                mag_H_db = self.math_utils.mag_H_db(H_z)
            line = mag_H_db
            self._set_freq_resp_title("Resposta em Frequência: Magnitude (dB)")
            self._set_mag_checkbox()
        else:
            if self.var_normalize.get():
                mag_H = self.math_utils.mag_H_norm(H_z)
            else:
                mag_H = self.math_utils.mag_H(H_z)
            line = mag_H
            self._set_freq_resp_title("Resposta em Frequência: Magnitude")
            self._set_mag_checkbox()

        self.line_r.set_data(w_plot, line)

        # X limit
        x_max = theta_val*np.pi
        self.ax_r.set_xlim(0, x_max)

        # Auto scale
        self.ax_r.set_ylim(auto=True)
        self.ax_r.relim()
        self.ax_r.autoscale_view()

        self.canvas_r.draw_idle()

    def _set_phase_checkbox(self):
        self.check_normalize.pack_forget()
        self.check_phase_unit.pack(side="left", padx=10)

    def _set_mag_checkbox(self):
        self.check_phase_unit.pack_forget()
        self.check_normalize.pack(side="left", padx=10)

    def _set_freq_resp_title(self, title):
        self.ax_r.set_title(
            title,
            color=color_text,
            fontsize=10,
            pad=10,
            loc="left"
        )

    def _create_fr_fig(self, width):
        fr = tk.Frame(
            self.main_container,
            width=width,
            height=360,
            bg=color_bg
        )
        fr.pack(side="left", padx=10, pady=5)
        fr.pack_propagate(False)
        return fr

    def _create_menu(self):
        return tk.Menu(self.menubar, tearoff=False)

    def _create_label_fr(self, master, text, padx=10):
        fr = tk.LabelFrame(
            master,
            text=text,
            fg=color_text,
            bg=color_bg,
            bd=1,
            relief="raised",
            padx=padx,
            pady=5
        )
        fr.pack(side="left", padx=10, fill="y")
        return fr

#     def _create_spin_top(self, row, col, col_text, text):
#         tk.Label(
#             self.fr_limits,
#             text=text,
#             fg=color_text,
#             bg=color_bg
#         ).grid(row=row, column=col_text, padx=2, pady=2)
# 
#         spin = tk.Spinbox(
#             self.fr_limits,
#             from_=-1.5, to=1.5,
#             increment=0.1,
#             width=6,
#             bg=color_bg_spin,
#             fg=color_text,
#             insertbackground=color_text,
#             buttonbackground=color_bg
#         )
#         spin.grid(row=row, column=col, padx=5, pady=2)
#         return spin

    def _create_scrollable_fr(self, parent, width, height, bg_color):
        outer_fr = tk.Frame(parent, width=width, height=height, bg=bg_color)
        outer_fr.grid_propagate(False)

        canvas = tk.Canvas(outer_fr, bg=bg_color, highlightthickness=0)

        scrollbar = tk.Scrollbar(
            outer_fr,
            orient="vertical",
            command=canvas.yview
        )

        scrollable_fr = tk.Frame(canvas, bg=bg_color)
        scrollable_fr.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=(
                    0, 0,
                    scrollable_fr.winfo_reqwidth(),
                    scrollable_fr.winfo_reqheight())
                )
        )

        canvas.create_window((0, 0), window=scrollable_fr, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        outer_fr.grid_rowconfigure(0, weight=1)
        outer_fr.grid_columnconfigure(0, weight=1)
        outer_fr.grid_columnconfigure(1, weight=0)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind("<MouseWheel>", on_mousewheel)
        scrollable_fr.bind("<MouseWheel>", on_mousewheel)

        if not hasattr(self, "_scroll_refs"):
            self._scroll_refs = []
        self._scroll_refs.extend([canvas, scrollbar, scrollable_fr])

        return outer_fr, scrollable_fr

    def _create_label_coords(self, fr, text_var):
        tk.Label(
            fr,
            textvariable=text_var,
            bg=color_bg,
            font=("Arial", 8)
        ).pack(padx=2, pady=2)

    def _setup_point_plotter(self, marker, color):
        points_plot, = self.ax_p.plot(
            [],
            [],
            color=color,
            marker=marker,
            markerfacecolor="none",
            linestyle="none",
            markersize=7,
            markeredgewidth=1,
            zorder=2
        )
        return points_plot

    def _update_labels_coords(self):
        poles_text = ""
        for pair_p in self.poles.list:
            p1 = pair_p[0]
            sign_1 = "+" if p1.imag >= 0 else "-"
            poles_text += f"({p1.real:.3f} {sign_1} j{abs(p1.imag):.3f})"
            if len(pair_p) == 2:
                p2 = pair_p[1]
                sign_2 = "+" if p2.imag >= 0 else "-"
                poles_text += f" e ({p2.real:.3f} {sign_2} j{abs(p2.imag):.3f})\n"
            else:
                poles_text += "\n"

        zeros_text = ""
        for pair_z in self.zeros.list:
            z1 = pair_z[0]
            sign_1 = "+" if z1.imag >= 0 else "-"
            zeros_text += f"({z1.real:.3f} {sign_1} j{abs(z1.imag):.3f})"
            if len(pair_z) == 2:
                z2 = pair_z[1]
                sign_2 = "+" if z2.imag >= 0 else "-"
                zeros_text += f" e ({z2.real:.3f} {sign_2} j{abs(z2.imag):.3f})\n"
            else:
                zeros_text += "\n"

        poles_text = poles_text.strip()
        zeros_text = zeros_text.strip()

        # Keep width when empty
        if not poles_text:
            poles_text = 54*" "
        if not zeros_text:
            zeros_text = 54*" "

        self.text_poles_var.set(poles_text)
        self.text_zeros_var.set(zeros_text)

        self.fr_poles.update_idletasks()
        self.fr_zeros.update_idletasks()

    def _get_list_sel(self):
        if self.bt_states[self.icon_pole].get():
            list_sel = self.poles
        elif self.bt_states[self.icon_zero].get():
            list_sel = self.zeros
        return list_sel

    def _create_bts(self, list_bt, side):
        if side == "top":
            padx, pady = 5, 2
            pack_side = "left"
            pack_pady = 2
            container = self.toolbar
        else:  # left
            padx, pady = 6, 6
            pack_side = "top"
            container = self.fr_bt_left

        last_group = None
        for i, (key, (hint, group, starts_active)) in enumerate(list_bt):
            if isinstance(key, str):
                img_icon = None
                text = key
            else:
                img_icon = key
                text = None

            var = tk.BooleanVar(value=starts_active)

            self.bt_states[key] = var
            self.bt_groups[key] = group

            # Keep buttons from the same group together
            extra_pad = 0
            if (side == "top" and
                last_group is not None and
                group != last_group
            ):
                extra_pad = 10
            last_group = group

            if side == "left":
                pack_pady = (60, 3) if i == 0 else 3

            bt = tk.Checkbutton(
                container,
                image=img_icon,
                text=text,
                variable=var,
                indicatoron=False,
                selectcolor=color_bt_selected,
                relief="flat",
                bg=color_bg,
                padx=padx,
                pady=pady,
                command=lambda k=key: self._on_button_click(k)
            )

            if side == "top":
                bt.pack(side=pack_side, padx=(2+extra_pad, 2), pady=pack_pady)
            else:  # left
                bt.pack(side=pack_side, fill="x", pady=pack_pady)

    def _on_button_click(self, clicked_key):
        v_clicked     = self.bt_states[clicked_key]
        group_clicked = self.bt_groups[clicked_key]

        if group_clicked != -1:
            # Do not toggle when clicking on an already active button
            if not v_clicked.get():
                v_clicked.set(True)
                return

            # Unclick other buttons from the same group
            for key, group in self.bt_groups.items():
                if key != clicked_key and group == group_clicked:
                    self.bt_states[key].set(False)

        # hint = self.dict_bt[clicked_key][0]

        if clicked_key in (self.icon_freq, self.icon_freq_db, self.icon_phase):
            self.update_freq_resp()
        elif clicked_key == self.icon_clear:
            self.clear_poles_zeros()
            self.update_all()
            v_clicked.set(False)
        elif clicked_key == self.icon_kb:
            self._open_kb_dialog()
            v_clicked.set(False)
        elif clicked_key == self.icon_3d:
            Plotter3D(self.win, self)
            v_clicked.set(False)
        elif clicked_key == self.icon_info:
            self._open_sys_clf_info()
            v_clicked.set(False)
        elif clicked_key == self.icon_plane:
            self.tf_displayer.update_labels()
            self.tf_displayer.show_labels()
        elif clicked_key == "FT":
            self.tf_displayer.show_entries()
        elif clicked_key in (
            self.icon_open,
            self.icon_save,
            self.icon_plane_top,
            self.icon_imp,
            self.icon_deg,
            "S",
        ):
            self._show_warning("Ainda não implementado")
            v_clicked.set(False)

    def _on_z_inv_click(self):
        if self.bt_states[self.icon_plane].get():
            self.tf_displayer.update_labels()
        self.tf_displayer.invert_z_entries()

    def clear_poles_zeros(self):
        self.poles.clear()
        self.zeros.clear()

    def center_toplevel(self, tl):
        # Center Toplevel acording to the Main Window
        self.win.update_idletasks()

        win_x = self.win.winfo_x()
        win_y = self.win.winfo_y()

        win_w = self.win.winfo_width()
        win_h = self.win.winfo_height()

        popup_w = tl.winfo_width()
        popup_h = tl.winfo_height()

        x = win_x + (win_w // 2) - (popup_w // 2)
        y = win_y + (win_h // 2) - (popup_h // 2)

        tl.geometry(f"+{x}+{y}")

    def _map_elements(self):
        list_coords = []
        list_mapping = []  # ("p"|"z", idx_in_list)

        for i, pair_p in enumerate(self.poles.list):
            for p in pair_p:
                list_coords.append([p.real, p.imag])
                list_mapping.append(("p", i))
        for i, pair_z in enumerate(self.zeros.list):
            for p in pair_z:
                list_coords.append([p.real, p.imag])
                list_mapping.append(("z", i))

        return list_coords, list_mapping

    def _on_click(self, event):
        if self.toolbar_p.mode != "" or event.inaxes != self.ax_p:
            return

        list_coords, list_mapping = self._map_elements()

        # Calculate distance to prevent duplicated
        dist = np.array([])
        if len(list_coords) > 0:
            coords = np.array(list_coords)
            click = np.array([event.xdata, event.ydata])
            dist = np.sqrt(np.sum((coords - click)**2, axis=1))
        next = (len(dist) > 0 and np.min(dist) < range_click)

        # Right button
        if event.button == R_BUTTON:
            if next:
                idx = np.argmin(dist)
                element_type, idx_group = list_mapping[idx]
                if element_type == "p":
                    self.poles.pop(idx_group)
                else:  # "z"
                    self.zeros.pop(idx_group)

                self.update_all()

        # Left button
        elif event.button == L_BUTTON:
            list_sel = self._get_list_sel()

            if next:
                idx = np.argmin(dist)
                element_type, idx_group = list_mapping[idx]

                if element_type == "p":
                    self.idx_sel_point = idx_group
                    self.type_sel_point = "p"
                elif element_type == "z":
                    self.idx_sel_point = idx_group
                    self.type_sel_point = "z"
                else:
                    self.idx_sel_point = None
                    self.type_sel_point = None
            else:
                self.add_element_plane(list_sel, event.xdata, event.ydata)
                self.update_all()

                if list_sel == self.poles:
                    self.idx_sel_point = self.poles.num_pairs() - 1
                    self.type_sel_point = "p"
                elif list_sel == self.zeros:
                    self.idx_sel_point = self.zeros.num_pairs() - 1
                    self.type_sel_point = "z"

    def _on_move(self, event):
        if (event.button is not None and
            self.idx_sel_point is not None and
            event.inaxes == self.ax_p
        ):
            event_x = event.xdata
            event_y = event.ydata

            if self.type_sel_point == "p":
                target_list = self.poles.list
            else:  # "z"
                target_list = self.zeros.list

            current_group = target_list[self.idx_sel_point]

            if len(current_group) == 2:
                p1 = complex(event_x, event_y)
                p2 = complex(event_x, -event_y)
                target_list[self.idx_sel_point] = (p1, p2)
            else:
                p_real = complex(event_x, 0)
                target_list[self.idx_sel_point] = (p_real,)

            self.update_all()

    def _on_drop(self, event):
        self.idx_sel_point = None
        self.type_sel_point = None

    def update_all(self):
        self.update_plane()
        self.update_freq_resp()
        self._update_labels_coords()
        self._update_stats()
        self._update_sys_clf()
        if self.bt_states[self.icon_plane].get():
            self.tf_displayer.update_labels()

    def _update_stats(self):
        text = (
            f"Polos: {self.poles.num_elements()}\n"
            f"Zeros: {self.zeros.num_elements()}"
        )
        self.label_stats.config(text=text)

    def _update_sys_clf(self):
        text, bg = self.system_classifier.update()
        if bg is None:
            bg = color_bg
        self.label_system.config(text=text)
        self.label_system.config(bg=bg)

    def update_plane(self):
        if not self.poles.empty():
            list_x_poles = []
            list_y_poles = []
            for pair_p in self.poles.list:
                for p in pair_p:
                    list_x_poles.append(p.real)
                    list_y_poles.append(p.imag)

            self.points_plot_poles.set_data(list_x_poles, list_y_poles)
        else:
            self.points_plot_poles.set_data([], [])

        if not self.zeros.empty():
            list_x_zeros = []
            list_y_zeros = []
            for pair_z in self.zeros.list:
                for z in pair_z:
                    list_x_zeros.append(z.real)
                    list_y_zeros.append(z.imag)
            self.points_plot_zeros.set_data(list_x_zeros, list_y_zeros)
        else:
            self.points_plot_zeros.set_data([], [])

        self.canvas_p.draw_idle()

    def run(self):
        self.win.mainloop()
