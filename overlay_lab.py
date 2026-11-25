from __future__ import annotations

import tkinter as tk
from tkinter import ttk

APP_TITLE = "ROB RUN | Overlay Lab"
BG = "#101722"
PANEL = "#172231"
TEXT = "#e8eef7"
MUTED = "#91a3b8"
CYAN = "#45d7ff"
GREEN = "#a8ff54"
RED = "#ff6969"


class OverlayLab:
    """Standalone visual overlay demo using synthetic entities only.

    It deliberately does not inspect game memory, processes, files, network
    traffic, screenshots, or anti-cheat state.
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("440x570")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.flags = {
            "players": tk.BooleanVar(value=True),
            "skeleton": tk.BooleanVar(value=True),
            "distance": tk.BooleanVar(value=True),
            "vehicles": tk.BooleanVar(value=True),
            "items": tk.BooleanVar(value=True),
            "crosshair": tk.BooleanVar(value=True),
        }
        self.opacity = tk.DoubleVar(value=0.88)
        self.overlay: tk.Toplevel | None = None
        self.canvas: tk.Canvas | None = None
        self._style()
        self._build_panel()
        self._open_overlay()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 19, "bold"), foreground="white")
        style.configure("Muted.TLabel", foreground=MUTED)
        style.configure("TCheckbutton", background=BG, foreground=TEXT, font=("Segoe UI", 10))
        style.map("TCheckbutton", background=[("active", BG)], foreground=[("active", "white")])
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)

    def _build_panel(self) -> None:
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="OVERLAY LAB", style="Title.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Visualizador independente • dados fictícios", style="Muted.TLabel").pack(anchor="w", pady=(3, 15))

        notice = tk.Label(
            outer,
            text="MODO DEMONSTRAÇÃO\nO overlay usa entidades sintéticas. Não lê nem se conecta ao ROB RUN.",
            bg="#243247", fg="#c8d8ea", justify="left", anchor="w",
            padx=12, pady=10, font=("Segoe UI", 9), wraplength=380,
        )
        notice.pack(fill="x", pady=(0, 16))

        ttk.Label(outer, text="ELEMENTOS DO OVERLAY").pack(anchor="w", pady=(0, 8))
        grid = ttk.Frame(outer)
        grid.pack(fill="x")
        options = [
            ("players", "Player labels"),
            ("skeleton", "Skeleton"),
            ("distance", "Distance"),
            ("vehicles", "Vehicles"),
            ("items", "Equipment labels"),
            ("crosshair", "Crosshair"),
        ]
        for index, (key, label) in enumerate(options):
            ttk.Checkbutton(grid, text=label, variable=self.flags[key], command=self.redraw).grid(
                row=index // 2, column=index % 2, sticky="w", padx=(0, 12), pady=7
            )

        ttk.Separator(outer).pack(fill="x", pady=16)
        ttk.Label(outer, text="TRANSPARÊNCIA").pack(anchor="w")
        scale = tk.Scale(
            outer, from_=0.35, to=1.0, resolution=0.01, orient="horizontal",
            variable=self.opacity, command=self.set_opacity,
            bg=BG, fg=TEXT, troughcolor="#34465d", highlightthickness=0,
            activebackground=CYAN, bd=0,
        )
        scale.pack(fill="x", pady=(3, 12))

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=(5, 0))
        ttk.Button(actions, text="Mostrar / ocultar overlay", command=self.toggle_overlay).pack(side="left")
        ttk.Button(actions, text="Reabrir overlay", command=self._open_overlay).pack(side="right")

        ttk.Label(
            outer,
            text="Dica: arraste a janela do overlay pela faixa superior. Feche por aqui para encerrar tudo.",
            style="Muted.TLabel", wraplength=390, justify="left",
        ).pack(anchor="w", pady=(17, 0))

    def _open_overlay(self) -> None:
        if self.overlay is not None and self.overlay.winfo_exists():
            self.overlay.deiconify()
            self.overlay.lift()
            self.redraw()
            return
        win = tk.Toplevel(self.root)
        self.overlay = win
        win.title("Overlay Lab Preview")
        win.geometry("760x460+520+120")
        win.attributes("-topmost", True)
        win.attributes("-alpha", self.opacity.get())
        win.configure(bg="#121212")
        win.resizable(True, True)

        titlebar = tk.Frame(win, bg="#172231", height=28)
        titlebar.pack(fill="x")
        tk.Label(titlebar, text="  OVERLAY LAB  /  SYNTHETIC SCENE", bg="#172231", fg=CYAN,
                 font=("Segoe UI", 8, "bold")).pack(side="left", pady=5)
        tk.Label(titlebar, text="DEMO DATA  •  DRAG TO MOVE", bg="#172231", fg=MUTED,
                 font=("Segoe UI", 8)).pack(side="right", padx=10)
        titlebar.bind("<ButtonPress-1>", self._drag_start)
        titlebar.bind("<B1-Motion>", self._drag_move)
        for child in titlebar.winfo_children():
            child.bind("<ButtonPress-1>", self._drag_start)
            child.bind("<B1-Motion>", self._drag_move)

        self.canvas = tk.Canvas(win, bg="#242b32", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _event: self.redraw())
        self.redraw()

    def _drag_start(self, event: tk.Event) -> None:
        self._drag_x = event.x_root - self.overlay.winfo_x()
        self._drag_y = event.y_root - self.overlay.winfo_y()

    def _drag_move(self, event: tk.Event) -> None:
        if self.overlay:
            self.overlay.geometry(f"+{event.x_root - self._drag_x}+{event.y_root - self._drag_y}")

    def set_opacity(self, _value: str) -> None:
        if self.overlay is not None and self.overlay.winfo_exists():
            self.overlay.attributes("-alpha", self.opacity.get())

    def toggle_overlay(self) -> None:
        if self.overlay is None or not self.overlay.winfo_exists():
            self._open_overlay()
        elif self.overlay.state() == "withdrawn":
            self.overlay.deiconify()
            self.overlay.lift()
        else:
            self.overlay.withdraw()

    def redraw(self) -> None:
        if self.canvas is None or not self.canvas.winfo_exists():
            return
        c = self.canvas
        c.delete("all")
        w = max(c.winfo_width(), 400)
        h = max(c.winfo_height(), 260)

        # Neutral synthetic scene backdrop, not a game capture.
        c.create_rectangle(0, h * .63, w, h, fill="#303840", outline="")
        c.create_polygon(0, h * .63, w * .48, h * .48, w, h * .62, w, h * .70, 0, h * .72,
                         fill="#3d454b", outline="")
        c.create_text(14, 12, anchor="nw", text="CENA FICTÍCIA • SEM LEITURA DO JOGO",
                      fill="#aab8c8", font=("Segoe UI", 9, "bold"))

        people = [
            (w * .27, h * .43, "Player_01", "31.4 m", "SCARLET ATOM"),
            (w * .54, h * .39, "Player_02", "18.2 m", "HUBBER"),
            (w * .78, h * .45, "Player_03", "42.7 m", "PADONOK"),
        ]
        for x, y, name, distance, item in people:
            if self.flags["skeleton"].get():
                c.create_line(x, y + 12, x, y + 53, fill=CYAN, width=2)
                c.create_line(x, y + 23, x - 13, y + 38, fill=CYAN, width=2)
                c.create_line(x, y + 23, x + 13, y + 38, fill=CYAN, width=2)
                c.create_line(x, y + 53, x - 11, y + 75, fill=CYAN, width=2)
                c.create_line(x, y + 53, x + 11, y + 75, fill=CYAN, width=2)
                c.create_oval(x - 6, y, x + 6, y + 12, outline=CYAN, width=2)
            if self.flags["players"].get():
                c.create_text(x, y - 27, text=name, fill="white", font=("Segoe UI", 9, "bold"))
            if self.flags["distance"].get():
                c.create_text(x, y + 88, text=distance, fill=GREEN, font=("Segoe UI", 8, "bold"))
            if self.flags["items"].get():
                c.create_text(x, y + 103, text=item, fill=CYAN, font=("Segoe UI", 8))

        if self.flags["vehicles"].get():
            for x, y, label in [(w * .40, h * .73, "VEHICLE • DEMO"), (w * .72, h * .72, "VEHICLE • DEMO")]:
                c.create_rectangle(x - 65, y - 22, x + 65, y + 22, outline=GREEN, width=2)
                c.create_text(x, y - 34, text=label, fill=GREEN, font=("Segoe UI", 8, "bold"))
                c.create_oval(x - 48, y + 15, x - 25, y + 38, outline="#dce6f2", width=2)
                c.create_oval(x + 25, y + 15, x + 48, y + 38, outline="#dce6f2", width=2)

        if self.flags["crosshair"].get():
            cx, cy = w / 2, h / 2
            c.create_line(cx - 13, cy, cx + 13, cy, fill="white", width=2)
            c.create_line(cx, cy - 13, cx, cy + 13, fill="white", width=2)
            c.create_oval(cx - 28, cy - 28, cx + 28, cy + 28, outline="#a9b7c6")

        c.create_text(w - 12, h - 10, anchor="se", text="ROB RUN OVERLAY LAB • LOCAL DEMO",
                      fill="#b9c8d7", font=("Segoe UI", 8))

    def close(self) -> None:
        if self.overlay is not None and self.overlay.winfo_exists():
            self.overlay.destroy()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    OverlayLab(root)
    root.mainloop()


if __name__ == "__main__":
    main()
