import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import zipfile
import os
import threading

# ── Colours & fonts ──────────────────────────────────────────────
BG        = "#0F1F3D"
CARD      = "#1A2F52"
ACCENT    = "#1E4DB7"
ACCENT2   = "#C8922A"
TEXT      = "#FFFFFF"
TEXT_DIM  = "#8A96A8"
SUCCESS   = "#22C55E"
DANGER    = "#EF4444"
FONT      = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_LG   = ("Segoe UI", 14, "bold")
FONT_SM   = ("Segoe UI", 9)


def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024**2):.1f} MB"
    else:
        return f"{size_bytes / (1024**3):.2f} GB"


def get_total_size(paths):
    total = 0
    for p in paths:
        if os.path.isfile(p):
            total += os.path.getsize(p)
        elif os.path.isdir(p):
            for dirpath, _, filenames in os.walk(p):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    try:
                        total += os.path.getsize(fp)
                    except OSError:
                        pass
    return total


class FileCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FileZip — File Compressor")
        self.root.geometry("680x600")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.files = []
        self.output_path = tk.StringVar(value="")

        self._build_ui()

    def _build_ui(self):
        hdr = tk.Frame(self.root, bg=BG, pady=20)
        hdr.pack(fill="x", padx=30)

        tk.Label(hdr, text="📦", font=("Segoe UI", 28), bg=BG, fg=ACCENT2).pack(side="left")
        title_frame = tk.Frame(hdr, bg=BG)
        title_frame.pack(side="left", padx=12)
        tk.Label(title_frame, text="FileZip", font=("Segoe UI", 20, "bold"), bg=BG, fg=TEXT).pack(anchor="w")
        tk.Label(title_frame, text="Compress files & folders into ZIP archives",
                 font=FONT_SM, bg=BG, fg=TEXT_DIM).pack(anchor="w")

        self._build_file_zone()
        self._build_output_section()
        self._build_bottom()

    def _build_file_zone(self):
        card = tk.Frame(self.root, bg=CARD, bd=0, relief="flat")
        card.pack(fill="x", padx=30, pady=(0, 14))

        row = tk.Frame(card, bg=CARD, pady=10, padx=16)
        row.pack(fill="x")
        tk.Label(row, text="Files to Compress", font=FONT_BOLD, bg=CARD, fg=TEXT).pack(side="left")

        btn_frame = tk.Frame(row, bg=CARD)
        btn_frame.pack(side="right")

        tk.Button(btn_frame, text="+ Add Files", font=FONT_SM, bg=ACCENT, fg=TEXT,
                  relief="flat", padx=10, pady=4, cursor="hand2",
                  command=self.add_files).pack(side="left", padx=(0, 6))
        tk.Button(btn_frame, text="+ Add Folder", font=FONT_SM, bg=ACCENT, fg=TEXT,
                  relief="flat", padx=10, pady=4, cursor="hand2",
                  command=self.add_folder).pack(side="left", padx=(0, 6))
        tk.Button(btn_frame, text="Clear All", font=FONT_SM, bg="#2A3F6B", fg=TEXT_DIM,
                  relief="flat", padx=10, pady=4, cursor="hand2",
                  command=self.clear_files).pack(side="left")

        tk.Frame(card, bg="#243356", height=1).pack(fill="x")

        list_frame = tk.Frame(card, bg=CARD, padx=16, pady=10)
        list_frame.pack(fill="both")

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", bg=CARD)
        self.listbox = tk.Listbox(
            list_frame, font=FONT_SM, bg=CARD, fg=TEXT,
            selectbackground=ACCENT, selectforeground=TEXT,
            relief="flat", bd=0, height=8,
            yscrollcommand=scrollbar.set,
            activestyle="none"
        )
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.pack(fill="both", expand=True)

        self.empty_label = tk.Label(
            list_frame, text="No files added yet.\nClick '+ Add Files' or '+ Add Folder' to get started.",
            font=FONT_SM, bg=CARD, fg=TEXT_DIM, justify="center"
        )
        self.empty_label.place(relx=0.5, rely=0.5, anchor="center")

        tk.Button(card, text="✕  Remove Selected", font=FONT_SM, bg=CARD, fg=DANGER,
                  relief="flat", pady=6, cursor="hand2",
                  command=self.remove_selected).pack(anchor="e", padx=16, pady=(0, 10))

    def _build_output_section(self):
        card = tk.Frame(self.root, bg=CARD)
        card.pack(fill="x", padx=30, pady=(0, 14))

        row = tk.Frame(card, bg=CARD, padx=16, pady=12)
        row.pack(fill="x")

        tk.Label(row, text="Save ZIP as", font=FONT_BOLD, bg=CARD, fg=TEXT, width=12, anchor="w").pack(side="left")

        self.output_entry = tk.Entry(
            row, textvariable=self.output_path, font=FONT_SM,
            bg="#243356", fg=TEXT, insertbackground=TEXT,
            relief="flat", bd=0
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(8, 8), ipady=6, ipadx=6)

        tk.Button(row, text="Browse", font=FONT_SM, bg=ACCENT, fg=TEXT,
                  relief="flat", padx=10, pady=4, cursor="hand2",
                  command=self.browse_output).pack(side="left")

    def _build_bottom(self):
        bottom = tk.Frame(self.root, bg=BG)
        bottom.pack(fill="x", padx=30, pady=(0, 20))

        self.progress = ttk.Progressbar(bottom, orient="horizontal", mode="determinate", length=620)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TProgressbar", troughcolor=CARD, background=ACCENT, thickness=6)
        self.progress.pack(fill="x", pady=(0, 12))

        stats_row = tk.Frame(bottom, bg=BG)
        stats_row.pack(fill="x", pady=(0, 12))

        self.lbl_original = tk.Label(stats_row, text="Original: —", font=FONT_SM, bg=BG, fg=TEXT_DIM)
        self.lbl_original.pack(side="left")

        self.lbl_compressed = tk.Label(stats_row, text="Compressed: —", font=FONT_SM, bg=BG, fg=TEXT_DIM)
        self.lbl_compressed.pack(side="left", padx=20)

        self.lbl_saved = tk.Label(stats_row, text="Saved: —", font=FONT_SM, bg=BG, fg=TEXT_DIM)
        self.lbl_saved.pack(side="left")

        self.lbl_status = tk.Label(bottom, text="", font=FONT_SM, bg=BG, fg=TEXT_DIM)
        self.lbl_status.pack(anchor="w", pady=(0, 10))

        self.btn_compress = tk.Button(
            bottom, text="🗜  Compress to ZIP", font=("Segoe UI", 12, "bold"),
            bg=ACCENT2, fg=TEXT, relief="flat", padx=24, pady=12,
            cursor="hand2", command=self.start_compress
        )
        self.btn_compress.pack(fill="x")

    def add_files(self):
        paths = filedialog.askopenfilenames(title="Select Files")
        for p in paths:
            if p not in self.files:
                self.files.append(p)
        self._refresh_list()

    def add_folder(self):
        path = filedialog.askdirectory(title="Select Folder")
        if path and path not in self.files:
            self.files.append(path)
        self._refresh_list()

    def clear_files(self):
        self.files.clear()
        self._refresh_list()

    def remove_selected(self):
        selected = self.listbox.curselection()
        for i in reversed(selected):
            del self.files[i]
        self._refresh_list()

    def browse_output(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip")],
            title="Save ZIP file as"
        )
        if path:
            self.output_path.set(path)

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        if self.files:
            self.empty_label.place_forget()
            for f in self.files:
                icon = "📁" if os.path.isdir(f) else "📄"
                self.listbox.insert(tk.END, f"  {icon}  {f}")
        else:
            self.empty_label.place(relx=0.5, rely=0.5, anchor="center")

    def start_compress(self):
        if not self.files:
            messagebox.showwarning("No Files", "Please add at least one file or folder.")
            return
        if not self.output_path.get():
            messagebox.showwarning("No Output", "Please choose where to save the ZIP file.")
            return
        threading.Thread(target=self._compress, daemon=True).start()

    def _compress(self):
        self.btn_compress.config(state="disabled", text="Compressing...")
        self.lbl_status.config(text="Calculating size...", fg=TEXT_DIM)
        self.progress["value"] = 0

        original_size = get_total_size(self.files)
        self.lbl_original.config(text=f"Original: {format_size(original_size)}")

        output = self.output_path.get()

        all_files = []
        for path in self.files:
            if os.path.isfile(path):
                all_files.append((path, os.path.basename(path)))
            elif os.path.isdir(path):
                folder_name = os.path.basename(path)
                for dirpath, _, filenames in os.walk(path):
                    for f in filenames:
                        full = os.path.join(dirpath, f)
                        arcname = os.path.join(folder_name, os.path.relpath(full, path))
                        all_files.append((full, arcname))

        total = len(all_files)

        try:
            with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
                for i, (full_path, arcname) in enumerate(all_files):
                    zf.write(full_path, arcname)
                    progress = int((i + 1) / total * 100)
                    self.progress["value"] = progress
                    self.lbl_status.config(text=f"Compressing {i+1}/{total}: {os.path.basename(full_path)}")
                    self.root.update_idletasks()

            compressed_size = os.path.getsize(output)
            saved = original_size - compressed_size
            ratio = (saved / original_size * 100) if original_size > 0 else 0

            self.lbl_compressed.config(text=f"Compressed: {format_size(compressed_size)}")
            self.lbl_saved.config(
                text=f"Saved: {format_size(saved)} ({ratio:.1f}%)",
                fg=SUCCESS if saved > 0 else TEXT_DIM
            )
            self.lbl_status.config(
                text=f"✅ Done! Saved to: {output}",
                fg=SUCCESS
            )
            self.progress["value"] = 100

        except Exception as e:
            self.lbl_status.config(text=f"❌ Error: {str(e)}", fg=DANGER)
            self.progress["value"] = 0

        finally:
            self.btn_compress.config(state="normal", text="🗜  Compress to ZIP")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileCompressorApp(root)
    root.mainloop()
