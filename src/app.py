# Copyright 2026 Omar Zagonel El Laden
# SPDX-License-Identifier: GPL-3.0-only

import os
import tkinter as tk

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


icon_logo_path = os.path.join("icons", "logo.png")

range_click = 0.1

max_pi = 4

init_resolution = 500
max_resolution = 1000

dpi = 100

ax_text_pos = 1.6
lim_plane = 1.3
lw = 1.5
win_size = "1000x600"

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


        self.menu_file     = self._create_menu()
        self.menu_edit     = self._create_menu()
        self.menu_entry    = self._create_menu()
        self.menu_plane    = self._create_menu()
        self.menu_system   = self._create_menu()
        self.menu_graphics = self._create_menu()
        self.menu_windows  = self._create_menu()
        self.menu_help     = self._create_menu()

        self.menu_graphics.add_command(label="Cores", command=self._open_color_dialog)

        self.menu_help.add_command(label="Ajuda", command=self._open_help_dialog)
        self.menu_help.add_command(label="Sobre", command=self._open_about_dialog)


        self.menubar.add_cascade(label="Arquivo", menu=self.menu_file)
        self.menubar.add_cascade(label="Editar", menu=self.menu_edit)
        self.menubar.add_cascade(label="Entrada de Raízes", menu=self.menu_entry)
        self.menubar.add_cascade(label="Plano", menu=self.menu_plane)
        self.menubar.add_cascade(label="Sistema", menu=self.menu_system)
        self.menubar.add_cascade(label="Gráficos", menu=self.menu_graphics)
        self.menubar.add_cascade(label="Janelas", menu=self.menu_windows)
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
        self.icon_zoom = self._create_icon("zoom.png", 3)
        self.icon_hand = self._create_icon("hand.png", 3)
        self.icon_dim = self._create_icon("dim.png", 3)
        self.icon_clear = self._create_icon("clear.png", 3)
        self.icon_info = self._create_icon("info.png", 3)

        self.icon_exit = self._create_icon("exit.png", 6)
        self.icon_graphic = self._create_icon("graphic.png", 6)
        self.icon_save_as = self._create_icon("save_as.png", 6)

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
            self.icon_imp: ("Resposta ao Impulso", 2, False),
            self.icon_deg: ("Resposta ao Degrau Unitário", 2, False),
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

        self.frame_top = tk.Frame(self.win, bg=color_bg, pady=5)
        self.frame_top.pack(side="top", fill="x", padx=10)

        self.main_container = tk.Frame(self.win, bg=color_bg)
        self.main_container.pack(
            side="top",
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=5
        )

        # Left Buttons
        self.frame_bt_left = tk.Frame(self.main_container, bg=color_bg)
        self.frame_bt_left.pack(side="left", fill="y", padx=5, pady=5)
        self._create_bts(list(self.dict_bt.items())[13:], "left")


        # Poles and zeros

        self.list_poles = []
        self.list_zeros = []

        box_poles = self._create_label_frame(self.frame_top, "Polos")
        box_zeros = self._create_label_frame(self.frame_top, "Zeros")

        frame_poles_outer, self.frame_poles = self._create_scrollable_frame(
            box_poles,
            width=200,
            height=45,
            bg_color=color_bg
        )
        frame_poles_outer.pack(side="left", padx=5, pady=5)

        frame_zeros_outer, self.frame_zeros = self._create_scrollable_frame(
            box_zeros,
            width=200,
            height=45,
            bg_color=color_bg
        )
        frame_zeros_outer.pack(side="left", padx=5, pady=5)

        self.text_poles_var = tk.StringVar()
        self.text_zeros_var = tk.StringVar()

        self._create_label_coords(self.frame_poles, self.text_poles_var)
        self._create_label_coords(self.frame_zeros, self.text_zeros_var)


#         self.frame_limits = self._create_label_frame(
#             self.frame_top,
#             "Limites do Plano"
#         )
#         self.spin_a = self._create_spin_top(0, 1, 0, "Eixo X")
#         self.spin_b = self._create_spin_top(0, 3, 2, "a")
#         self.spin_c = self._create_spin_top(1, 1, 0, "Eixo Y")
#         self.spin_d = self._create_spin_top(1, 3, 2, "a")


#         entry = tk.Entry(
#             self.frame_bottom,
#             width=20,
#             bg="#151515",
#             fg="white",
#             insertbackground="white"
#         )
#         color_text.pack(side="left")


        # Bottom Frame

        self.frame_bottom = tk.Frame(self.win, bg=color_bg, pady=4)
        self.frame_bottom.pack(side="bottom", fill="x", padx=10)

        # z inv checkbox
        self.var_z_inv = tk.BooleanVar(value=True)
        self.check_z_inv = tk.Checkbutton(
            self.frame_bottom,
            text="z⁻ⁿ",
            variable=self.var_z_inv,
            bg=color_bg,
            fg=color_text,
            selectcolor=color_bg_spin,
            activebackground=color_bg,
            activeforeground=color_text,
            command=self._update_label_tf
        )
        self.check_z_inv.pack(side="left", padx=10)

        # Transfer Function equation

        label_funct = self._create_label_frame(
            self.frame_bottom,
            "Função de transferência"
        )

        self.label_hz = self._create_label_frame_text(label_funct, "H(z) = 1")

        # Figure Frames
        self.frame_plane = self._create_frame_fig(width=360)
        self.frame_resp  = self._create_frame_fig(width=600)


        # Plane Figure

        self.fig_p = Figure(figsize=(2.8, 2.8), dpi=dpi, facecolor=color_bg)
        self.ax_p = self.fig_p.add_subplot()
        self.ax_p.set_facecolor(color_z_bg)
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
        self.ax_p.axhline(0, color=color_ln, lw=lw, zorder=1)
        self.ax_p.axvline(0, color=color_ln, lw=lw, zorder=1)
        circle = patches.Circle(
            xy=(0, 0),
            radius=1,
            color=color_ln,
            fill=False,
            lw=lw,
            zorder=1
        )
        self.ax_p.add_patch(circle)

        self.points_plot_poles = self._setup_point_plotter("x", color_poles)
        self.points_plot_zeros = self._setup_point_plotter("o", color_zeros)

        self.idx_sel_point = None

        self.canvas_p = FigureCanvasTkAgg(self.fig_p, master=self.frame_plane)
        self.canvas_p.draw()

        # Matplotlib toolbar
        self.toolbar_p = NavigationToolbar2Tk(
            self.canvas_p,
            window=self.frame_plane,
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
            self.frame_plane,
            text="",  # "Sistema Realizável e Estável",
            fg=color_text,
            bg=color_bg,
            font=("Arial", 8),
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
        self.ax_r.set_facecolor(color_z_bg)
        self.ax_r.grid(True, color=color_grid, linestyle="--")
        self.ax_r.tick_params(colors=color_text)
        self.ax_r.set_ylim(-1, 1)
        self._set_freq_resp_title("Resposta em Frequência: Magnitude")

        self.line_r, = self.ax_r.plot([], [], color=color_resp, linewidth=2)

        # Set x ticks as multiples of pi
        step = 0.5 * np.pi
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

        self.canvas_r = FigureCanvasTkAgg(self.fig_r, master=self.frame_resp)
        self.canvas_r.draw()

        # Matplotlib toolbar
        self.toolbar_r = NavigationToolbar2Tk(
            self.canvas_r,
            window=self.frame_resp,
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

        self.frame_input_r = tk.Frame(self.frame_resp, bg=color_bg, pady=5)
        self.frame_input_r.pack(side="top", fill="x")

        frame_r_padx = 2

        # Theta Spin

        tk.Label(
            self.frame_input_r,
            text="θₘₐₓ =",
            fg=color_text,
            bg=color_bg
        ).pack(side="left", padx=frame_r_padx)

        self.theta_max = tk.Spinbox(
            self.frame_input_r,
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
        self.theta_max.pack(side="left", padx=frame_r_padx)

        tk.Label(
            self.frame_input_r,
            text="π",
            fg=color_text,
            bg=color_bg
        ).pack(side="left", padx=frame_r_padx)

        # Normalized checkbox
        self.var_normalize = tk.BooleanVar(value=True)
        self.check_normalize = tk.Checkbutton(
            self.frame_input_r,
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
            self.frame_input_r,
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
            self.frame_input_r,
            text="pts",
            fg=color_text,
            bg=color_bg
        ).pack(side="right", padx=frame_r_padx)

        self.resolution = tk.Spinbox(
            self.frame_input_r,
            from_=10, to=1000,
            increment=10,
            width=4,
            textvariable=tk.DoubleVar(value=init_resolution),
            bg=color_bg_spin,
            fg=color_text,
            insertbackground=color_text,
            buttonbackground=color_bg,
            command=self._change_resolution
        )
        self.resolution.pack(side="right", padx=frame_r_padx)

        tk.Label(
            self.frame_input_r,
            text="Resolução =",
            fg=color_text,
            bg=color_bg
        ).pack(side="right", padx=frame_r_padx)

        # Events to confirm keyboard values
        self.resolution.bind("<Return>",   lambda event: self._change_resolution())
        self.resolution.bind("<FocusOut>", lambda event: self._change_resolution())

        self._update_all()

    def _create_icon(self, filename, reduction=18):
        file_path = os.path.join("icons", filename)
        if os.path.isfile(file_path):
            try:
                img = tk.PhotoImage(file=file_path)
                img = img.subsample(reduction, reduction)
                return img
            except Exception as e:
                print(f"Error loading image '{file_path}': {e}")

    def update_colors(self, key, new_color):
#         if key == "curve":
#             self.line.set_color(new_color)
#         elif key == "grid":
#             self.ax.grid(True, color=new_color)
#         elif chave == "bg":
#             self.fig.patch.set_facecolor(new_color)
#             self.ax.set_facecolor(new_color)
# 
#         self.canvas.draw_idle()
        pass

    def _open_kb_dialog(self):
        KBDialog(self.win, self)

    def _open_color_dialog(self):
        ColorDialog(self.win, self)

    def _open_about_dialog(self):
        AboutDialog(self.win, self)

    def _open_help_dialog(self):
        HelpDialog(self.win, self)

    def add_element_plane(self, list_sel, x, y):
        if list_sel is None:
            print("Failed to insert")
            return

        list_sel.append((x, y))
        list_sel.append((x, -y))

        self._update_all()

    def _change_resolution(self):
        resolution = self.resolution.get()
        if resolution.isdigit() and int(resolution) <= max_resolution:
            self.math_utils.resolution = int(self.resolution.get())
            self.update_freq_resp()
        else:
            self.resolution.delete(0, "end")
            self.resolution.insert(0, str(self.math_utils.resolution))

    def update_freq_resp(self):
        theta_val = int(self.theta_max.get())
        self.math_utils.max_pi = theta_val

        w_plot = self.math_utils.get_w_plot()
        H_z = self.math_utils.calc_H(self.list_zeros, self.list_poles)

        # Select what to plot
        if self.bt_states[self.icon_phase].get():
            if self.var_phase_deg.get():
                ang_H = self.math_utils.calc_phase_H_deg(H_z)
                self._set_freq_resp_title("Resposta em Frequência: Fase (graus)")
            else:
                ang_H = self.math_utils.calc_phase_H_rad(H_z)
                self._set_freq_resp_title("Resposta em Frequência: Fase (rad)")
            line = ang_H
            self._set_phase_checkbox()
        elif self.bt_states[self.icon_freq_db].get():
            if self.var_normalize.get():
                mag_H_db = self.math_utils.calc_mag_H_db_norm(H_z)
            else:
                mag_H_db = self.math_utils.calc_mag_H_db(H_z)
            line = mag_H_db
            self._set_freq_resp_title("Resposta em Frequência: Magnitude (dB)")
            self._set_mag_checkbox()
        else:
            if self.var_normalize.get():
                mag_H = self.math_utils.calc_mag_H_norm(H_z)
            else:
                mag_H = self.math_utils.calc_mag_H(H_z)
            line = mag_H
            self._set_freq_resp_title("Resposta em Frequência: Magnitude")
            self._set_mag_checkbox()

        self.line_r.set_data(w_plot, line)

        # X limit
        x_max = theta_val * np.pi
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

    def _create_frame_fig(self, width):
        frame = tk.Frame(
            self.main_container,
            width=width,
            height=360,
            bg=color_bg
        )
        frame.pack(side="left", padx=10, pady=5)
        frame.pack_propagate(False)
        return frame

    def _create_menu(self):
        return tk.Menu(self.menubar, tearoff=False)

    def _create_label_frame(self, master, text, padx=10):
        frame = tk.LabelFrame(
            master,
            text=text,
            fg=color_text,
            bg=color_bg,
            bd=1,
            relief="raised",
            padx=padx,
            pady=5
        )
        frame.pack(side="left", padx=10, fill="y")
        return frame

#     def _create_spin_top(self, row, col, col_text, text):
#         tk.Label(
#             self.frame_limits,
#             text=text,
#             fg=color_text,
#             bg=color_bg
#         ).grid(row=row, column=col_text, padx=2, pady=2)
# 
#         spin = tk.Spinbox(
#             self.frame_limits,
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

    def _create_scrollable_frame(self, parent, width, height, bg_color):
        outer_frame = tk.Frame(parent, width=width, height=height, bg=bg_color)
        outer_frame.grid_propagate(False)

        canvas = tk.Canvas(outer_frame, bg=bg_color, highlightthickness=0)

        scrollbar = tk.Scrollbar(
            outer_frame,
            orient="vertical",
            command=canvas.yview
        )

        scrollable_frame = tk.Frame(canvas, bg=bg_color)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=(
                    0, 0,
                    scrollable_frame.winfo_reqwidth(),
                    scrollable_frame.winfo_reqheight())
                )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        outer_frame.grid_rowconfigure(0, weight=1)
        outer_frame.grid_columnconfigure(0, weight=1)
        outer_frame.grid_columnconfigure(1, weight=0)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", on_mousewheel)

        if not hasattr(self, "_scroll_refs"):
            self._scroll_refs = []
        self._scroll_refs.extend([canvas, scrollbar, scrollable_frame])

        return outer_frame, scrollable_frame

    def _create_label_coords(self, frame, text_var):
        tk.Label(
            frame,
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

    def _create_label_frame_text(self, master, text):
        label = tk.Label(
            master,
            text=text,
            fg=color_text,
            bg=color_bg,
            font=("Consolas", 11)
        )
        label.pack(expand=True)
        return label

    def _update_labels_coords(self):
        poles_text = ""
        for i in range(0, len(self.list_poles), 2):
            if i + 1 < len(self.list_poles):
                pole = self.list_poles[i]
                pole_text = f"({pole[0]:.3f} + j{abs(pole[1]):.3f})"
                poles_text += f"{pole_text}"
                conj = self.list_poles[i+1]
                if pole[0] == conj[0] and pole[1] == conj[1]:
                    poles_text += "\n"
                else:
                    poles_text += f" e {pole_text.replace('+', '-')}\n"

        zeros_text = ""
        for i in range(0, len(self.list_zeros), 2):
            if i + 1 < len(self.list_zeros):
                zero = self.list_zeros[i]
                zero_text = f"({zero[0]:.3f} + j{abs(zero[1]):.3f})"
                zeros_text += f"{zero_text}"
                conj = self.list_zeros[i+1]
                if zero[0] == conj[0] and zero[1] == conj[1]:
                    zeros_text += "\n"
                else:
                    zeros_text += f" e {zero_text.replace('+', '-')}\n"

        poles_text = poles_text.strip()
        zeros_text = zeros_text.strip()

        # Keep width when empty
        if not poles_text:
            poles_text = 54*" "
        if not zeros_text:
            zeros_text = 54*" "

        self.text_poles_var.set(poles_text)
        self.text_zeros_var.set(zeros_text)

        self.frame_poles.update_idletasks()
        self.frame_zeros.update_idletasks()

    def _update_label_tf(self):
        if self.var_z_inv.get():
            eq = self.math_utils.format_H_z_inv(self.list_zeros, self.list_poles)
        else:
            eq = self.math_utils.format_H_z(self.list_zeros, self.list_poles)
        self.label_hz.config(text=eq)

    def _get_list_sel(self):
        if self.bt_states[self.icon_pole].get():
            list_sel = self.list_poles
        elif self.bt_states[self.icon_zero].get():
            list_sel = self.list_zeros
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
            container = self.frame_bt_left

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
            self._clear_poles_zeros()
            self._update_all()
            v_clicked.set(False)
        elif clicked_key == self.icon_kb:
            self._open_kb_dialog()
            v_clicked.set(False)
        elif clicked_key == self.icon_3d:
            Plotter3D(self.win, self)
            v_clicked.set(False)

    def _clear_poles_zeros(self):
        self.list_poles = []
        self.list_zeros = []

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

    def _on_click(self, event):
        if self.toolbar_p.mode != "" or event.inaxes != self.ax_p:
            return

        list_poles_zeros = self.list_poles + self.list_zeros

        # Calculate distance to prevent duplicated
        dist = np.array([])
        if len(list_poles_zeros) > 0:
            coords = np.array(list_poles_zeros)
            click = np.array([event.xdata, event.ydata])
            dist = np.sqrt(np.sum((coords - click) ** 2, axis=1))

        next = (len(dist) > 0 and np.min(dist) < range_click)

        # Right button
        if event.button == R_BUTTON:
            if next:
                idx = np.argmin(dist)
                len_poles = len(self.list_poles)

                if idx < len_poles:
                    idx_start = idx if (idx % 2 == 0) else (idx - 1)

                    self.list_poles.pop(idx_start + 1)
                    self.list_poles.pop(idx_start)
                else:
                    idx_rel = idx - len_poles
                    if (idx_rel % 2 == 0):
                        idx_start = idx_rel
                    else:
                        idx_start = idx_rel-1

                    self.list_zeros.pop(idx_start + 1)
                    self.list_zeros.pop(idx_start)

                self._update_all()

        # Left button
        elif event.button == L_BUTTON:
            list_sel = self._get_list_sel()

            if next:
                idx = np.argmin(dist)
                len_poles = len(self.list_poles)

                if list_sel == self.list_poles and idx < len_poles:
                    self.idx_sel_point = idx
                    self.type_sel_point = "pole"
                elif list_sel == self.list_zeros and idx >= len_poles:
                    self.idx_sel_point = idx - len_poles
                    self.type_sel_point = "zero"
                else:
                    self.idx_sel_point = None
                    self.type_sel_point = None
            else:
                self.add_element_plane(list_sel, event.xdata, event.ydata)
                self.idx_sel_point = len(list_sel) - 1

                if list_sel == self.list_poles:
                    self.type_sel_point = "pole"
                elif list_sel == self.list_zeros:
                    self.type_sel_point = "zero"

    def _on_move(self, event):
        if (event.button is not None and
            self.idx_sel_point is not None and
            event.inaxes == self.ax_p
        ):
            event_x = event.xdata
            event_y = event.ydata

            if self.type_sel_point == "pole":
                target_list = self.list_poles
            else:
                target_list = self.list_zeros

            target_list[self.idx_sel_point] = (event_x, event_y)

            if self.idx_sel_point % 2 == 0:
                conj_idx = self.idx_sel_point + 1
            else:
                conj_idx = self.idx_sel_point - 1

            if conj_idx < len(target_list):
                target_list[conj_idx] = (event_x, -event_y)

            self._update_all()

    def _on_drop(self, event):
        self.idx_sel_point = None
        self.type_sel_point = None

    def _update_all(self):
        self.update_plane()
        self.update_freq_resp()
        self._update_labels_coords()
        self._update_label_tf()

    def update_plane(self):
        if self.list_poles:
            x_poles, y_poles = zip(*self.list_poles)
            self.points_plot_poles.set_data(x_poles, y_poles)
        else:
            self.points_plot_poles.set_data([], [])

        if self.list_zeros:
            x_zeros, y_zeros = zip(*self.list_zeros)
            self.points_plot_zeros.set_data(x_zeros, y_zeros)
        else:
            self.points_plot_zeros.set_data([], [])

        self.canvas_p.draw_idle()

    def run(self):
        self.win.mainloop()
