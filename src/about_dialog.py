import tkinter as tk

from configs import *


class AboutDialog:
    def __init__(self, parent, app):
        # Toplevel
        tl = tk.Toplevel(parent)
        tl.title("Sobre")
        tl.geometry("400x200")
        tl.configure(bg=color_bg)
        tl.resizable(False, False)
        tl.transient(parent)
        tl.grab_set()

        app.center_toplevel(tl)

        # Text
        tk.Label(
            tl,
            text=app_name,
            fg=color_text,
            bg=color_bg,
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        tk.Label(tl, text=app_version, fg="gray", bg=color_bg).pack()
        tk.Label(tl, text=app_description, fg="gray", bg=color_bg).pack()
        tk.Label(tl, text=app_copyright, fg=color_text, bg=color_bg).pack(pady=10)
        tk.Label(tl, text=app_license, fg=color_text, bg=color_bg).pack()

        tk.Button(tl, text="Close", command=tl.destroy, width=10).pack(pady=10)
