"""Cross-platform Acropalypse recovery GUI (Python 3.10+)."""
from __future__ import annotations

import os
import platform
import queue
import tempfile
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk
from acropalypse import Acropalypse
from gif_lib import acropalypse_gif

PRESETS = {
    "Custom RGB": (1920, 1080, False),
    "Custom RGBA": (1920, 1080, True),
    "Windows 11 Snipping Tool": (1920, 1080, True),
    "Google Pixel 3": (1080, 2160, False),
    "Google Pixel 3 XL": (1440, 2960, False),
    "Google Pixel 3a": (1080, 2220, False),
    "Google Pixel 3a XL": (1080, 2160, False),
    "Google Pixel 4": (1080, 2280, False),
    "Google Pixel 4 XL": (1440, 3040, False),
    "Google Pixel 4a": (1080, 2340, False),
    "Google Pixel 5": (1080, 2340, False),
    "Google Pixel 5a": (1080, 2400, False),
    "Google Pixel 6": (1080, 2400, False),
    "Google Pixel 6 Pro": (1440, 3120, False),
    "Google Pixel 6a": (1080, 2400, False),
    "Google Pixel 7": (1080, 2400, False),
    "Google Pixel 7 Pro": (1440, 3120, False),
}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Acropalypse Multi-Tool")
        self.geometry("1120x760")
        self.minsize(850, 600)
        self.configure(bg="#171923")
        self.acro = Acropalypse()
        self.input_path: Path | None = None
        self.output_path: Path | None = None
        self.preview_refs = []
        self.events: queue.Queue = queue.Queue()
        self._build_style()
        self._build_ui()
        self.after(100, self._poll_events)

    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(".", font=("Segoe UI", 10))
        style.configure("TFrame", background="#171923")
        style.configure("Panel.TFrame", background="#222635")
        style.configure("TLabel", background="#171923", foreground="#edf0f7")
        style.configure("Muted.TLabel", background="#222635", foreground="#aab2c5")
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground="#ffffff")
        style.configure("Subtitle.TLabel", foreground="#aab2c5")
        style.configure("TButton", padding=(12, 8), background="#343d54", foreground="#ffffff")
        style.map("TButton", background=[("active", "#465574"), ("disabled", "#292f3e")])
        style.configure("Accent.TButton", background="#5577d8", foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#6689ed")])
        style.configure("TEntry", fieldbackground="#2b3040", foreground="#ffffff", insertcolor="white", padding=7)
        style.configure("TCombobox", fieldbackground="#2b3040", foreground="#ffffff", padding=7)
        style.configure("TNotebook", background="#171923", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(18, 10), background="#222635", foreground="#cbd2e1")
        style.map("TNotebook.Tab", background=[("selected", "#343d54")], foreground=[("selected", "#ffffff")])
        style.configure("Treeview", background="#222635", fieldbackground="#222635", foreground="#edf0f7", rowheight=28)
        style.configure("Treeview.Heading", background="#343d54", foreground="white")
        style.configure("Horizontal.TProgressbar", troughcolor="#2b3040", background="#6689ed")

    def _build_ui(self):
        header = ttk.Frame(self, padding=(24, 20, 24, 12))
        header.pack(fill="x")
        ttk.Label(header, text="Acropalypse Multi-Tool", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Détection et reconstruction d’images PNG / GIF vulnérables", style="Subtitle.TLabel").pack(anchor="w", pady=(4, 0))
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=(4, 18))
        self.detect_tab = ttk.Frame(self.tabs, padding=18)
        self.restore_tab = ttk.Frame(self.tabs, padding=18)
        self.tabs.add(self.detect_tab, text="  Détection  ")
        self.tabs.add(self.restore_tab, text="  Reconstruction  ")
        self._build_detection()
        self._build_restore()
        self.status = tk.StringVar(value="Prêt")
        ttk.Label(self, textvariable=self.status, anchor="w", padding=(22, 8), style="Subtitle.TLabel").pack(fill="x")

    def _build_detection(self):
        top = ttk.Frame(self.detect_tab)
        top.pack(fill="x", pady=(0, 12))
        ttk.Label(top, text="Rechercher les fichiers suspects", font=("Segoe UI", 14, "bold")).pack(side="left")
        ttk.Button(top, text="Choisir un dossier…", style="Accent.TButton", command=self.scan_folder).pack(side="right")
        ttk.Label(self.detect_tab, text="Analyse récursive des fichiers PNG et GIF. Double-cliquez sur un résultat pour l’ouvrir.", style="Muted.TLabel").pack(anchor="w", pady=(0, 12))
        columns = ("type", "path")
        self.results = ttk.Treeview(self.detect_tab, columns=columns, show="headings")
        self.results.heading("type", text="Format")
        self.results.heading("path", text="Fichier potentiellement vulnérable")
        self.results.column("type", width=90, stretch=False)
        self.results.column("path", width=800)
        scroll = ttk.Scrollbar(self.detect_tab, orient="vertical", command=self.results.yview)
        self.results.configure(yscrollcommand=scroll.set)
        self.results.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.results.bind("<Double-1>", self.open_result)
        self.scan_count = tk.StringVar(value="Aucun scan effectué")
        ttk.Label(self.detect_tab, textvariable=self.scan_count, style="Muted.TLabel").pack(anchor="w", pady=(10, 0))

    def _build_restore(self):
        toolbar = ttk.Frame(self.restore_tab)
        toolbar.pack(fill="x", pady=(0, 14))
        ttk.Button(toolbar, text="Ouvrir une image…", style="Accent.TButton", command=self.choose_image).pack(side="left")
        self.file_label = ttk.Label(toolbar, text="Aucune image sélectionnée", style="Muted.TLabel")
        self.file_label.pack(side="left", padx=12)
        settings = ttk.Frame(self.restore_tab, style="Panel.TFrame", padding=14)
        settings.pack(fill="x", pady=(0, 14))
        ttk.Label(settings, text="Profil de capture", style="Muted.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.preset = tk.StringVar(value="Custom RGB")
        combo = ttk.Combobox(settings, textvariable=self.preset, values=list(PRESETS), state="readonly", width=31)
        combo.grid(row=1, column=0, sticky="ew", padx=(0, 18), pady=(5, 0))
        combo.bind("<<ComboboxSelected>>", self.apply_preset)
        ttk.Label(settings, text="Largeur originale", style="Muted.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Label(settings, text="Hauteur originale", style="Muted.TLabel").grid(row=0, column=2, sticky="w", padx=(12, 0))
        self.width = tk.StringVar(value="1920")
        self.height = tk.StringVar(value="1080")
        ttk.Entry(settings, textvariable=self.width, width=12).grid(row=1, column=1, sticky="ew", pady=(5, 0))
        ttk.Entry(settings, textvariable=self.height, width=12).grid(row=1, column=2, sticky="ew", padx=(12, 0), pady=(5, 0))
        settings.columnconfigure(0, weight=2)
        settings.columnconfigure(1, weight=1)
        settings.columnconfigure(2, weight=1)
        actions = ttk.Frame(self.restore_tab)
        actions.pack(fill="x", pady=(0, 12))
        self.restore_btn = ttk.Button(actions, text="Reconstruire l’image", style="Accent.TButton", command=self.start_restore)
        self.restore_btn.pack(side="left")
        self.save_btn = ttk.Button(actions, text="Enregistrer le résultat…", command=self.save_result, state="disabled")
        self.save_btn.pack(side="left", padx=10)
        self.progress = ttk.Progressbar(actions, mode="indeterminate", length=180)
        self.progress.pack(side="right")
        previews = ttk.Frame(self.restore_tab)
        previews.pack(fill="both", expand=True)
        self.original_panel = self._preview_panel(previews, "Image source")
        self.restored_panel = self._preview_panel(previews, "Image reconstruite")
        previews.columnconfigure(0, weight=1)
        previews.columnconfigure(1, weight=1)
        previews.rowconfigure(0, weight=1)

    def _preview_panel(self, parent, title):
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=12)
        # caller positions panels after creation
        idx = 0 if title == "Image source" else 1
        panel.grid(row=0, column=idx, sticky="nsew", padx=(0, 6) if idx == 0 else (6, 0))
        ttk.Label(panel, text=title, style="Muted.TLabel").pack(anchor="w")
        label = ttk.Label(panel, text="Aperçu indisponible", style="Muted.TLabel", anchor="center")
        label.pack(fill="both", expand=True, pady=8)
        if idx == 0:
            self.original_preview = label
        else:
            self.restored_preview = label
        return panel

    def apply_preset(self, _event=None):
        w, h, _alpha = PRESETS[self.preset.get()]
        self.width.set(str(w))
        self.height.set(str(h))

    def choose_image(self):
        name = filedialog.askopenfilename(filetypes=[("Images PNG/GIF", "*.png *.gif"), ("Tous les fichiers", "*.*")])
        if not name:
            return
        self.input_path = Path(name)
        self.output_path = None
        self.file_label.configure(text=self.input_path.name)
        self.save_btn.configure(state="disabled")
        self._show_preview(self.input_path, self.original_preview)
        self.restored_preview.configure(image="", text="En attente de reconstruction")
        self.restored_preview.image = None
        self.status.set("Image chargée. Vérifiez le profil et les dimensions.")

    def _show_preview(self, path, target):
        try:
            with Image.open(path) as im:
                im.seek(0)
                preview = im.convert("RGBA")
                preview.thumbnail((520, 360))
            photo = ImageTk.PhotoImage(preview)
            target.configure(image=photo, text="")
            target.image = photo
        except Exception as exc:
            target.configure(image="", text=f"Aperçu impossible : {exc}")
            target.image = None

    def start_restore(self):
        if not self.input_path:
            messagebox.showinfo("Image requise", "Sélectionnez d’abord une image.")
            return
        try:
            w, h = int(self.width.get()), int(self.height.get())
            if not (1 <= w <= 65535 and 1 <= h <= 65535):
                raise ValueError
        except ValueError:
            messagebox.showerror("Dimensions invalides", "La largeur et la hauteur doivent être des entiers entre 1 et 65535.")
            return
        if self.input_path.suffix.lower() == ".gif" and acropalypse_gif is None:
            messagebox.showerror("Extension GIF absente", "Le module natif GIF n’est pas installé.\nConsultez BUILD.md pour le compiler sur Windows ou Linux.")
            return
        self.restore_btn.configure(state="disabled")
        self.save_btn.configure(state="disabled")
        self.progress.start(12)
        self.status.set("Reconstruction en cours…")
        source = self.input_path
        alpha = PRESETS[self.preset.get()][2]
        def worker():
            try:
                suffix = ".gif" if source.suffix.lower() == ".gif" else ".png"
                fd, output = tempfile.mkstemp(prefix="acropalypse_", suffix=suffix)
                os.close(fd)
                Path(output).unlink(missing_ok=True)
                if suffix == ".gif":
                    acropalypse_gif.restore(str(source), output, w, h)
                else:
                    self.acro.reconstruct_image(str(source), w, h, alpha, output_path=output)
                self.events.put(("restore_ok", output))
            except Exception as exc:
                self.events.put(("restore_error", str(exc)))
        threading.Thread(target=worker, daemon=True).start()

    def _poll_events(self):
        try:
            while True:
                kind, payload = self.events.get_nowait()
                if kind == "scan_done":
                    for item in self.results.get_children():
                        self.results.delete(item)
                    for path in payload:
                        self.results.insert("", "end", values=(Path(path).suffix[1:].upper(), path))
                    self.scan_count.set(f"{len(payload)} fichier(s) suspect(s) trouvé(s)")
                    self.status.set("Analyse terminée")
                elif kind == "scan_error":
                    messagebox.showerror("Erreur d’analyse", payload)
                    self.status.set("Échec de l’analyse")
                elif kind == "restore_ok":
                    self.output_path = Path(payload)
                    self._show_preview(self.output_path, self.restored_preview)
                    self.save_btn.configure(state="normal")
                    self.status.set(f"Reconstruction terminée : {self.output_path.name}")
                    self._finish_restore()
                elif kind == "restore_error":
                    messagebox.showerror("Échec de la reconstruction", payload)
                    self.status.set("La reconstruction a échoué")
                    self._finish_restore()
        except queue.Empty:
            pass
        self.after(100, self._poll_events)

    def _finish_restore(self):
        self.progress.stop()
        self.restore_btn.configure(state="normal")

    def scan_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        self.status.set("Analyse du dossier en cours…")
        def worker():
            found = []
            try:
                for base, _dirs, files in os.walk(folder):
                    for filename in files:
                        path = Path(base) / filename
                        suffix = path.suffix.lower()
                        try:
                            if suffix == ".png":
                                vulnerable = self.acro.detect_png(str(path))
                            elif suffix == ".gif" and acropalypse_gif is not None:
                                vulnerable = acropalypse_gif.detect(str(path))
                            else:
                                continue
                            if vulnerable:
                                found.append(str(path))
                        except Exception:
                            continue
                self.events.put(("scan_done", found))
            except Exception as exc:
                self.events.put(("scan_error", str(exc)))
        threading.Thread(target=worker, daemon=True).start()

    def open_result(self, _event=None):
        selection = self.results.selection()
        if not selection:
            return
        path = self.results.item(selection[0], "values")[1]
        try:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                import subprocess
                subprocess.Popen(["open", path])
            else:
                import subprocess
                subprocess.Popen(["xdg-open", path])
        except Exception as exc:
            messagebox.showerror("Ouverture impossible", str(exc))

    def save_result(self):
        if not self.output_path or not self.output_path.exists():
            return
        ext = self.output_path.suffix
        name = filedialog.asksaveasfilename(
            defaultextension=ext,
            initialfile=f"{self.input_path.stem}_reconstructed{ext}",
            filetypes=[(f"{ext[1:].upper()} files", f"*{ext}")],
        )
        if name:
            import shutil
            shutil.copy2(self.output_path, name)
            self.status.set(f"Image enregistrée : {name}")


if __name__ == "__main__":
    App().mainloop()
