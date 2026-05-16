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


        # Top buttons

        icons_top = [
            self.icon_open,
            self.icon_save,
            self.icon_plane,
            "FT",
            self.icon_plane_top,
            "S",
            "Z",
            self.icon_freq,
            self.icon_freq_db,
            self.icon_phase,
            self.icon_imp,
            self.icon_deg,
            self.icon_3d,
        ]

        self.btn_states_top = {}
        for i, icon in enumerate(icons_top):
            if isinstance(icon, str):
                img_icon = None
                text = icon
            else:
                img_icon = icon
                text = None

            var = tk.BooleanVar(value=False)
            self.btn_states_top[f"btn_{i}"] = var

            btn = tk.Checkbutton(
                self.toolbar,
                image=img_icon,
                text=text,
                variable=var,
                indicatoron=False,
                selectcolor=color_bt_selected,
                relief="flat",
                bg=color_bg,
                padx=5,
                pady=2,
                command=lambda i=icon, v=var: print(f"{i} {'ON' if v.get() else 'OFF'}")
            )

            btn.pack(side="left", padx=2, pady=2)
        self.toolbar.pack(side="top", fill="x")


        self.frame_top = tk.Frame(self.window, bg=color_bg, pady=5)
        self.frame_top.pack(side="top", fill="x", padx=10)


        def create_label_frame(master, text, padx=10):
            frame = tk.LabelFrame(
                master=master,
                text=text,
                fg=color_fg_text,
                bg=color_bg,
                bd=1,
                relief="solid",
                padx=padx,
                pady=5
            )
            frame.pack(side="left", padx=10, fill="y")
            return frame

        def create_label_frame_text(master, text):
            label = tk.Label(
                master, text=text,
                fg=color_fg_text, bg=color_bg, font=("Segoe UI", 9)  # , "bold")
            )
            label.pack(expand=True)

        def create_spin_top(row, col, col_text, text):
            tk.Label(
                frame_limits,
                text=text,
                fg=color_fg_text,
                bg=color_bg
            ).grid(row=row, column=col_text, padx=2, pady=2)

            spin = tk.Spinbox(
                frame_limits,
                from_=-10.0, to=10.0,
                increment=0.1,
                width=6,
                bg=color_bg_spin,
                fg=color_fg_text,
                insertbackground=color_fg_text,
                buttonbackground=color_bg
            )
            spin.grid(row=row, column=col, padx=5, pady=2)

            return spin

        frame_poles  = create_label_frame(self.frame_top, "Pólos")
        frame_zeros  = create_label_frame(self.frame_top, "Zeros")
        frame_limits = create_label_frame(self.frame_top, "Limites do Plano")

        create_label_frame_text(frame_poles, "(0,535 + j0,490) e (0,535 - j0,490)\n(0,354 + j0,867) e (0,354 - j0,867)")
        create_label_frame_text(frame_zeros, "(0,143 + j0,972) e (0,143 - j0,972)\n(-0,445 + j0,912) e (-0,445 - j0,912)")

        self.spin_a = create_spin_top(0, 1, 0, "Eixo X")
        self.spin_b = create_spin_top(0, 3, 2, "a")
        self.spin_c = create_spin_top(1, 1, 0, "Eixo Y")
        self.spin_d = create_spin_top(1, 3, 2, "a")


        self.main_container = tk.Frame(self.window, bg=color_bg)
        self.main_container.pack(side="top", fill=tk.BOTH, expand=True, padx=10, pady=5)


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

        label_funct = create_label_frame(self.frame_bottom, "Função de transferência")

        create_label_frame_text(label_funct, "H(z)=1+0.604z^(-1)")


        # Left Buttons

        self.frame_bt_left = tk.Frame(self.main_container, bg=color_bg)
        self.frame_bt_left.pack(side="left", fill="y", padx=5, pady=5)

        icons_left = [
            self.icon_pole,
            self.icon_zero,
            self.icon_kb,
            self.icon_zoom,
            self.icon_hand,
            self.icon_dim,
            self.icon_clear,
            self.icon_info,
        ]

        self.btn_states_left = {}
        for i, icon in enumerate(icons_left):
            if isinstance(icon, str):
                img_icon = None
                text = icon
            else:
                img_icon = icon
                text = None

            var = tk.BooleanVar(value=False)
            self.btn_states_left[f"btn_v_{i}"] = var

            btn_v = tk.Checkbutton(
                self.frame_bt_left,
                image=img_icon,
                text=text,
                variable=var,
                indicatoron=False,
                selectcolor=color_bt_selected,
                relief="raised",
                bg=color_bg,
                padx=6, pady=6,
                command=lambda i=icon, v=var: print(f"Plane: {i} {'ON' if v.get() else 'OFF'}")
            )
            if i == 0:
                pady = (60, 3)
            else:
                pady = 3
            btn_v.pack(side="top", fill="x", pady=pady)



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
        self.ax_p.set_title("Plano z", color=color_fg_text, fontsize=12, pad=10, loc="left")

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

        # Poles and zeros
        self.x_data = []
        self.y_data = []
        self.points_plot, = self.ax_p.plot(
            [],
            [],
            color=color_poles,
            marker='x',
            linestyle='none',
            markersize=8,
            markeredgewidth=2,
            zorder=2
        )
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

        self.ax_r.set_title("Resposta em Frequência", color=color_fg_text, fontsize=12, pad=10, loc="left")
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
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

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

        # Calculate distance to prevent duplicated
        dist = np.array([])
        if len(self.x_data) > 0:
            dist = np.sqrt(
                (np.array(self.x_data) - event.xdata)**2 +
                (np.array(self.y_data) - event.ydata)**2
            )

        next = (len(dist) > 0 and np.min(dist) < 0.05)

        # Right button
        if event.button == R_BUTTON:
            if next:
                idx = np.argmin(dist)
                self.x_data.pop(idx)
                self.y_data.pop(idx)
                # self.status_str.set(f"Point {idx} removed")
                self.update_graphic()
            return

        # Left button
        if event.button == L_BUTTON:
            if next:
                self.idx_sel_point = np.argmin(dist)
            else:
                self.x_data.append(event.xdata)
                self.y_data.append(event.ydata)
                self.idx_sel_point = len(self.x_data) - 1
                self.update_graphic()

    def _on_move(self, event):
        if self.idx_sel_point is not None and event.inaxes == self.ax_p:
            self.x_data[self.idx_sel_point] = event.xdata
            self.y_data[self.idx_sel_point] = event.ydata
            self.update_graphic()

    def _on_drop(self, event):
        self.idx_sel_point = None

    def update_graphic(self):
        self.points_plot.set_data(self.x_data, self.y_data)
        self.canvas_p.draw_idle()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
