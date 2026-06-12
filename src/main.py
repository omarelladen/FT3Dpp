import os
import subprocess

import tkinter as tk
from tkinter import messagebox

import numpy as np

import matplotlib.patches as patches
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler

from configs import *


icon_logo_path = os.path.join("icons", "logo.png")

ax_text_pos = 1.6
lim = 1.5
lw = 1.5
win_size = "1200x800"

color_ln = "#00FF00"
color_bg = "#F0F0F0"  # "#212121"
color_z_bg = "#000000"
color_fg_text = "#000000"
color_grid = "#008000"
color_bg_spin = "#FFFFFF"
color_bt_selected = "#d1d1d1"
color_poles = "white"
color_zeros = "yellow"
color_resp = "white"

R_BUTTON = 3
L_BUTTON = 1


class App:
    def __init__(self):
        # Main Window
        self.window = tk.Tk()
        self.window.title(app_name)

        # Layout
        self.window.geometry(win_size)

        # Color
        self.window.configure(bg=color_bg)

        # Icon
        if os.name == "nt":  # Windows
            if os.path.isfile(icon_logo_path):
                try:
                    self.window.iconphoto(True, tk.PhotoImage(file=icon_logo_path))
                except Exception as e:
                    print(f"Error loading icon {icon_logo_path}: {e}")


        # Menu Bar
        small_font = ("Segoe UI", 8)
        self.menubar = tk.Menu(self.window, font=small_font)

        self.menu_file     = tk.Menu(self.menubar, tearoff=0)
        self.menu_edit     = tk.Menu(self.menubar, tearoff=0)
        self.menu_entry    = tk.Menu(self.menubar, tearoff=0)
        self.menu_plane    = tk.Menu(self.menubar, tearoff=0)
        self.menu_system   = tk.Menu(self.menubar, tearoff=0)
        self.menu_graphics = tk.Menu(self.menubar, tearoff=0)
        self.menu_windows  = tk.Menu(self.menubar, tearoff=0)

        # Help Menu
        self.menu_help = tk.Menu(self.menubar, tearoff=0)

        self.menu_help.add_command(label="Ajuda", command=lambda: self._show_info(dict_help, "Help",  "950x650", wraplength=900))
        self.menu_help.add_command(label="Sobre", command=self._show_about)


        # Add Help Menu to the Menu Bar
        self.menubar.add_cascade(label="Arquivo", menu=None)
        self.menubar.add_cascade(label="Editar", menu=None)
        self.menubar.add_cascade(label="Entrada de Raízes", menu=None)
        self.menubar.add_cascade(label="Plano", menu=None)
        self.menubar.add_cascade(label="Sistema", menu=None)
        self.menubar.add_cascade(label="Gráficos", menu=None)
        self.menubar.add_cascade(label="Janelas", menu=None)
        self.menubar.add_cascade(label="Ajuda", menu=self.menu_help)


        # Show Menu Bar
        self.window.config(menu=self.menubar)


        self.toolbar = tk.Frame(self.window, bd=1, relief="raised", bg=color_bg)

        def create_icon(filename, reduction=18):
            file_path = os.path.join("icons", filename)
            if os.path.isfile(file_path):
                try:
                    img = tk.PhotoImage(file=file_path).subsample(reduction, reduction)
                    return img
                except Exception as e:
                    print(f"Error loading image '{file_path}': {e}")

        # Icons

        self.icon_open = create_icon("open_t.png")
        self.icon_save = create_icon("save_t.png")
        self.icon_plane = create_icon("plane_t.png")
        self.icon_plane_top = create_icon("plane_top_t.png")
        self.icon_freq = create_icon("freq_t.png", 16)
        self.icon_freq_db = create_icon("freq_db_t.png", 16)
        self.icon_phase = create_icon("phase_t.png", 16)
        self.icon_imp = create_icon("imp_t.png", 16)
        self.icon_deg = create_icon("deg_t.png", 16)
        self.icon_3d = create_icon("3d_t.png", 16)

        self.icon_pole = create_icon("pole.png", 3)
        self.icon_zero = create_icon("zero.png", 3)
        self.icon_kb = create_icon("kb.png", 3)
        self.icon_zoom = create_icon("zoom.png", 3)
        self.icon_hand = create_icon("hand.png", 3)
        self.icon_dim = create_icon("dim.png", 3)
        self.icon_clear = create_icon("clear.png", 3)
        self.icon_info = create_icon("info.png", 3)

        self.icon_exit = create_icon("exit.png", 6)
        self.icon_graphic = create_icon("graphic.png", 6)
        self.icon_save_as = create_icon("save_as.png", 6)


        # Buttons

        self.dict_bt = {
            self.icon_open: ("Abrir Arquivo", -1, False),
            self.icon_save: ("Salvar Arquivo", -1, False),
            self.icon_plane: ("Entrada via Plano Complexo", 0, True),
            "FT": ("Entrada via Função de Transferência", 0, False),
            self.icon_plane_top: ("Topografia do Plano", -1, False),
            "S": ("Plano s", 1, False),
            "Z": ("Plano z", 1, True),
            self.icon_freq: ("Resposta em Frequência", 2, True),
            self.icon_freq_db: ("Resposta em Frequência em dB", 2, False),
            self.icon_phase: ("Fase", -1, False),
            self.icon_imp: ("Resposta ao Impulso", -1, False),
            self.icon_deg: ("Resposta ao Degrau Unitário", -1, False),
            self.icon_3d: ("Gráfico 3D", -1, False),

            self.icon_pole: ("Editar Pólos", 3, True),
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

        self.bt_states = {}  # {key: tk.BooleanVar}
        self.bt_groups = {}  # {key: group_id}


        # Top Buttons
        self._create_bts(list(self.dict_bt.items())[:13], "top")
        self.toolbar.pack(side="top", fill="x")

        self.frame_top = tk.Frame(self.window, bg=color_bg, pady=5)
        self.frame_top.pack(side="top", fill="x", padx=10)

        self.main_container = tk.Frame(self.window, bg=color_bg)
        self.main_container.pack(side="top", fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left Buttons
        self.frame_bt_left = tk.Frame(self.main_container, bg=color_bg)
        self.frame_bt_left.pack(side="left", fill="y", padx=5, pady=5)
        self._create_bts(list(self.dict_bt.items())[13:], "left")


        # Poles and zeros
        self.list_poles = []
        self.list_zeros = []


        box_poles = self._create_label_frame(self.frame_top, "Pólos")
        box_zeros = self._create_label_frame(self.frame_top, "Zeros")

        frame_poles_outer, self.frame_poles, self.canvas_poles = self._create_scrollable_frame(
            box_poles, width=200, height=100, bg_color=color_bg
        )
        frame_poles_outer.pack(side="left", padx=5, pady=5)

        frame_zeros_outer, self.frame_zeros, self.canvas_zeros = self._create_scrollable_frame(
            box_zeros, width=200, height=100, bg_color=color_bg
        )
        frame_zeros_outer.pack(side="left", padx=5, pady=5)


        self.text_poles_var = tk.StringVar()
        self.text_zeros_var = tk.StringVar()

        self._create_label_coords(self.frame_poles, self.text_poles_var)
        self._create_label_coords(self.frame_zeros, self.text_zeros_var)

        self._update_labels_text()


        self.frame_limits = self._create_label_frame(self.frame_top, "Limites do Plano")

        self.spin_a = self._create_spin_top(0, 1, 0, "Eixo X")
        self.spin_b = self._create_spin_top(0, 3, 2, "a")
        self.spin_c = self._create_spin_top(1, 1, 0, "Eixo Y")
        self.spin_d = self._create_spin_top(1, 3, 2, "a")


#         entry = tk.Entry(
#             self.frame_bottom,
#             width=20,
#             bg="#151515",
#             fg="white",
#             insertbackground="white"
#         )
#         color_fg_text.pack(side="left")


        self.frame_bottom = tk.Frame(self.window, bg=color_bg, pady=5)
        self.frame_bottom.pack(side="bottom", fill="x", padx=10)

        label_funct = self._create_label_frame(self.frame_bottom, "Função de transferência")

        self._create_label_frame_text(label_funct, "H(z)=1+0.604z^(-1)")


        self.frame_plane = tk.Frame(self.main_container, width=500, height=600, bg=color_bg)
        self.frame_plane.pack(side="left", padx=10, pady=5)
        self.frame_plane.pack_propagate(False)

        self.frame_resp = tk.Frame(self.main_container, width=500, height=550, bg=color_bg)
        self.frame_resp.pack(side="left", padx=10, pady=5)
        self.frame_resp.pack_propagate(False)


        # Plane Figure

        self.fig_p = Figure(figsize=(5, 5), dpi=100)
        self.ax_p = self.fig_p.add_subplot()
        self.ax_p.set_facecolor(color_z_bg)
        self.ax_p.set_xlim(-lim, lim)
        self.ax_p.set_ylim(-lim, lim)
        self.ax_p.set_aspect('equal')
        self.ax_p.set_title(
            "Plano z",
            color=color_fg_text,
            fontsize=12,
            pad=10,
            loc="left"
        )

        self.ax_p.text(
            0.5, 1.05,
            "Im",
            color=color_fg_text,
            fontsize=10,
            fontweight="bold",
            ha="center",
            va="bottom",
            transform=self.ax_p.transAxes
        )

        # Axis
        self.ax_p.text(
            1.05, 0.5,
            "Re",
            color=color_fg_text,
            fontsize=10,
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
        self.toolbar_p = NavigationToolbar2Tk(self.canvas_p, window=self.frame_plane, pack_toolbar=False)
        self.toolbar_p.update()

        self.canvas_p.get_tk_widget().pack(side="top", fill=tk.BOTH, expand=True)
        self.toolbar_p.pack(side="top", fill=tk.X)


        self.label_system = tk.Label(
            self.frame_plane,
            text="Sistema Realizável e Estável",
            fg=color_fg_text,
            bg=color_bg,
            font=("Segoe UI", 10),  # , "bold"),
            anchor="w",
            pady=10
        )
        self.label_system.pack(side="top", fill="x", padx=10)

        # Plane Events
        self.fig_p.canvas.mpl_connect('button_press_event',   self._on_click)
        self.fig_p.canvas.mpl_connect('motion_notify_event',  self._on_move)
        self.fig_p.canvas.mpl_connect('button_release_event', self._on_drop)


        # Frequency Response Figure

        self.fig_r = Figure(figsize=(5, 4), dpi=100, facecolor=color_bg)
        self.ax_r = self.fig_r.add_subplot()
        self.ax_r.set_facecolor(color_z_bg)

        t = np.linspace(0, 1.0, 500)  # 1s
        freq = 2
        sinal = np.sin(2*np.pi*freq*t)

        self.ax_r.plot(t, sinal, color=color_resp, linewidth=2)

        self.ax_r.set_title(
            "Resposta em Frequência",
            color=color_fg_text,
            fontsize=12,
            pad=10,
            loc="left"
        )
        self.ax_r.grid(True, color=color_grid, linestyle="--")
        self.ax_r.tick_params(colors=color_fg_text)
        self.ax_r.set_ylim(-1.2, 1.2)

        self.canvas_r = FigureCanvasTkAgg(self.fig_r, master=self.frame_resp)
        self.canvas_r.draw()

        # Matplotlib toolbar
        self.toolbar_r = NavigationToolbar2Tk(self.canvas_r, window=self.frame_resp, pack_toolbar=False)
        self.toolbar_r.update()

        self.canvas_r.get_tk_widget().pack(side="top", fill=tk.BOTH, expand=True)
        self.toolbar_r.pack(side="top", fill=tk.X)


        # Theta Spin

        self.frame_input_r = tk.Frame(self.frame_resp, bg=color_bg, pady=5)
        self.frame_input_r.pack(side="top", fill="x")

        tk.Label(
            self.frame_input_r,
            text="θₘₐₓ = ",
            fg=color_fg_text,
            bg=color_bg
        ).pack(side="left", padx=5)

        self.theta_max = tk.Spinbox(
            self.frame_input_r,
            from_=1.0, to=20.0,
            increment=0.5,
            width=12,
            bg=color_bg_spin,
            fg=color_fg_text,
            insertbackground=color_fg_text,
            buttonbackground=color_bg
        )
        self.theta_max.pack(side="left", padx=5)

        tk.Label(
            self.frame_input_r,
            text="π",
            fg=color_fg_text,
            bg=color_bg
        ).pack(side="left", padx=5)


    def _create_label_frame(self, master, text, padx=10):
        frame = tk.LabelFrame(
            master=master,
            text=text,
            fg=color_fg_text,
            bg=color_bg,
            bd=1,
            relief="raised",
            padx=padx,
            pady=5
        )
        frame.pack(side="left", padx=10, fill="y")
        return frame

    def _create_spin_top(self, row, col, col_text, text):
        tk.Label(
            self.frame_limits,
            text=text,
            fg=color_fg_text,
            bg=color_bg
        ).grid(row=row, column=col_text, padx=2, pady=2)

        spin = tk.Spinbox(
            self.frame_limits,
            from_=-1.5, to=1.5,
            increment=0.1,
            width=6,
            bg=color_bg_spin,
            fg=color_fg_text,
            insertbackground=color_fg_text,
            buttonbackground=color_bg
        )
        spin.grid(row=row, column=col, padx=5, pady=2)

        return spin

    def _create_scrollable_frame(self, parent, width, height, bg_color):
        outer_frame = tk.Frame(parent, width=width, height=height, bg=bg_color)
        outer_frame.grid_propagate(False)

        canvas = tk.Canvas(outer_frame, bg=bg_color, highlightthickness=0)

        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
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

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        if not hasattr(self, '_scroll_refs'):
            self._scroll_refs = []
        self._scroll_refs.extend([canvas, scrollbar, scrollable_frame])

        return outer_frame, scrollable_frame, canvas

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
            markersize=8,
            markeredgewidth=2,
            zorder=2
        )
        return points_plot

    def _create_label_frame_text(self, master, text):
        label = tk.Label(
            master, text=text,
            fg=color_fg_text, bg=color_bg, font=("Segoe UI", 9)  # , "bold")
        )
        label.pack(expand=True)

    def _update_labels_text(self):
        poles_text = ""
        for i in range(0, len(self.list_poles), 2):
            if i + 1 < len(self.list_poles):
                p1 = self.list_poles[i]
                p2 = self.list_poles[i+1]
                poles_text += f"({p1[0]:.3f} + j{abs(p1[1]):.3f}) e " \
                              f"({p2[0]:.3f} - j{abs(p2[1]):.3f})\n"

        zeros_text = ""
        for i in range(0, len(self.list_zeros), 2):
            if i + 1 < len(self.list_zeros):
                z1 = self.list_zeros[i]
                z2 = self.list_zeros[i+1]
                zeros_text += f"({z1[0]:.3f} + j{abs(z1[1]):.3f}) e " \
                              f"({z2[0]:.3f} - j{abs(z2[1]):.3f})\n"

        poles_text = poles_text.strip()
        zeros_text = zeros_text.strip()

        if not poles_text:
            poles_text = 54*" "
        if not zeros_text:
            zeros_text = 54*" "

        self.text_poles_var.set(poles_text)
        self.text_zeros_var.set(zeros_text)

        self.frame_poles.update_idletasks()
        self.frame_zeros.update_idletasks()

        self.canvas_poles.configure(scrollregion=self.canvas_poles.bbox("all"))
        self.canvas_zeros.configure(scrollregion=self.canvas_zeros.bbox("all"))


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
                bt.pack(side=pack_side, padx=2, pady=pack_pady)
            else:  # left
                bt.pack(side=pack_side, fill="x", pady=pack_pady)

    def _on_button_click(self, clicked_key):
        v_clicked = self.bt_states[clicked_key]
        group_clicked = self.bt_groups[clicked_key]

        if group_clicked != -1:
            if not v_clicked.get():
                v_clicked.set(True)
                return

            for key, group in self.bt_groups.items():
                if key != clicked_key and group == group_clicked:
                    self.bt_states[key].set(False)

        hint = self.dict_bt[clicked_key][0]
        print(f"'{hint}' -> {'ON' if v_clicked.get() else 'OFF'}")

    def _center_toplevel(self, tl):
        # Center Toplevel acording to the Main Window
        self.window.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width()  // 2) - (tl.winfo_width()  // 2)
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - (tl.winfo_height() // 2)
        tl.geometry(f"+{x}+{y}")

    def _show_about(self):
        # Toplevel
        tl = tk.Toplevel(self.window)
        tl.title("Sobre")
        tl.geometry("400x200")
        tl.configure(bg=color_bg)
        tl.resizable(False, False)
        tl.transient(self.window)
        tl.grab_set()

        self._center_toplevel(tl)

        # Text
        tk.Label(tl, text=app_name,        fg=color_fg_text, bg=color_bg, font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(tl, text=app_version,     fg="gray",  bg=color_bg).pack()
        tk.Label(tl, text=app_description, fg="gray",  bg=color_bg).pack()
        tk.Label(tl, text=app_copyright,   fg=color_fg_text, bg=color_bg).pack(pady=10)
        tk.Label(tl, text=app_license,     fg=color_fg_text, bg=color_bg).pack()

        tk.Button(tl, text="Close", command=tl.destroy, width=10).pack(pady=10)


    def _show_info(self, dict_info, title, size, wraplength):
        # Toplevel
        tl = tk.Toplevel(master=self.window)
        tl.title(title)
        tl.geometry(size)
        tl.configure(bg=color_bg)
        tl.transient(self.window)
        tl.grab_set()

        canvas = tk.Canvas(tl, bg=color_bg, highlightthickness=0)
        scrollbar = tk.Scrollbar(tl, orient="vertical", command=canvas.yview)

        # Frame with labels
        fr = tk.Frame(canvas, bg=color_bg, padx=20, pady=20)

        # Configure scroll
        fr.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Create the window inside the canvas for the frame
        canvas.create_window((0, 0), window=fr, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Layout
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Add info
        for name, desc in dict_info.items():
            label_name = tk.Label(master=fr, text=f"{name}:", fg=color_fg_text, bg=color_bg, anchor="w", font=("Arial", 12, "bold"))
            label_desc = tk.Label(master=fr, text=desc,       fg=color_fg_text, bg=color_bg, anchor="w", justify="left", wraplength=wraplength)

            label_name.pack(fill="x")
            label_desc.pack(fill="x", pady=(0, 10))

        # Add support for mouse scroll
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Close Button outside the canvas
        tk.Button(tl, text="Close", command=tl.destroy, width=10).pack(pady=10)

        self._center_toplevel(tl)

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

        next = (len(dist) > 0 and np.min(dist) < 0.05)

        # Right button
        if event.button == R_BUTTON:
            # TODO: fix bug that sometimes rm the wrong conjugate
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

                self._update_graphic()
            return

        # Left button
        if event.button == L_BUTTON:
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
                list_sel.append((event.xdata, event.ydata))
                list_sel.append((event.xdata, -event.ydata))

                self.idx_sel_point = len(list_sel) - 1

                if list_sel == self.list_poles:
                    self.type_sel_point = "pole"
                elif list_sel == self.list_zeros:
                    self.type_sel_point = "zero"
                self._update_graphic()

    def _on_move(self, event):
        if self.idx_sel_point is not None and event.inaxes == self.ax_p:
            if self.type_sel_point == "pole":
                self.list_poles[self.idx_sel_point] = (event.xdata, event.ydata)
                self.list_poles[self.idx_sel_point-1] = (event.xdata, -event.ydata)
            elif self.type_sel_point == "zero":
                self.list_zeros[self.idx_sel_point] = (event.xdata, event.ydata)
                self.list_zeros[self.idx_sel_point-1] = (event.xdata, -event.ydata)
            self._update_graphic()

    def _on_drop(self, event):
        self.idx_sel_point = None
        self.type_sel_point = None

    def _update_graphic(self):
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
        self._update_labels_text()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
