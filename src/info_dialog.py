import tkinter as tk

from configs import *


dict_help = {
    "FT": "Função de Transferência",
}


class InfoDialog:
    def __init__(self, parent, app):
        # Toplevel
        tl = tk.Toplevel(parent)
        tl.title("Ajuda")
        # tl.geometry("950x650")
        tl.configure(bg=color_bg)
        tl.transient(parent)
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
        for name, desc in dict_help.items():
            label_name = tk.Label(
                fr,
                text=f"{name}:",
                fg=color_text,
                bg=color_bg,
                anchor="w",
                font=("Arial", 12, "bold")
            )
            label_desc = tk.Label(
                fr,
                text=desc,
                fg=color_text,
                bg=color_bg,
                anchor="w",
                justify="left",
                wraplength=900
            )

            label_name.pack(fill="x")
            label_desc.pack(fill="x", pady=(0, 10))

        # Add support for mouse scroll
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Close Button outside the canvas
        tk.Button(tl, text="Close", command=tl.destroy, width=10).pack(pady=10)

        app.center_toplevel(tl)
