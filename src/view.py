import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from typing import Callable

class View(object):

    def __init__(self):
        self.callbacks = {}
        self.window = tk.Tk()
        self.window.title("PowerPoint Slide Exporter")
        self.window.resizable(False, False)

        self.sv_path = tk.StringVar(self.window, "")
        self.sv_slide = tk.StringVar(self.window, "")
        self.sv_max = tk.StringVar(self.window, "")

        self._show()

    def _show(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        frame.columnconfigure(0, weight=9)

        # PPTX File Selection
        browse_frame = tk.Frame(frame)
        browse_frame.grid(column=0, row=0, sticky="NSEW", pady=4)
        browse_frame.columnconfigure(0, weight=9)

        browse_label = tk.Label(browse_frame, width=50, relief="groove", anchor="w", textvariable=self.sv_path)
        browse_label.grid(column=0, row=0, sticky="NSEW", padx=4)
        
        browse_button = tk.Button(browse_frame, width=8, text="Browse", command=self.on_browse)
        browse_button.grid(column=1, row=0, sticky="NSEW", padx=4)

        # Export Parameters 
        param_frame = tk.Frame(frame)
        param_frame.grid(column=0, row=1, sticky="NSEW", pady=4)

        slide_frame = ttk.Labelframe(param_frame, text="Slide")
        slide_frame.grid(column=0, row=0, sticky="NSEW", padx=4, ipady=2)

        self.slide_entry = ttk.Spinbox(slide_frame, width=5, from_=1, textvariable=self.sv_slide)
        self.slide_entry.grid(column=0, row=0, sticky="NSEW", padx=4)

        tk.Label(slide_frame, text="/").grid(column=1, row=0, sticky="NSEW", padx=4)

        max_label = tk.Label(slide_frame, width=5, relief="groove", textvariable=self.sv_max)
        max_label.grid(column=2, row=0, sticky="NSEW", padx=4)

        # Buttons
        buttons_frame = tk.Frame(frame)
        buttons_frame.grid(column=0, row=2, sticky="NSEW", pady=4)
        buttons_frame.columnconfigure(0, weight=1, pad=20)

        self.auto_detect_button = tk.Button(buttons_frame, text="Auto Detect")
        self.auto_detect_button.grid(column=0, row=0, sticky="NSEW")

        self.export_button = tk.Button(buttons_frame, text="Export", command=self.on_export)
        self.export_button.grid(column=0, row=1, sticky="NSEW")

    def add_callbacks(self, callbacks: dict[str, Callable]):
        for key, callback in callbacks.items():
            self.callbacks[key] = callback

    def bind_callbacks(self):
        def slide_trace(*_):
            value = self.sv_slide.get()
            if "change_slide" in self.callbacks:
                self.callbacks["change_slide"](value)

        self.sv_slide.trace_add("write", slide_trace)
        self.auto_detect_button.config(command=self.callbacks["do_auto_detect"])

    def set_path(self, value: str):
        parts = value.split(os.sep)
        if len(parts) <= 1:
            self.sv_path.set(value)
            return
        trimmed = [parts[0], parts[-1]]
        for i in range(len(parts) - 2, 0, -1):
            if len(os.sep.join(trimmed)) + len(parts[i]) + 1 < 47:
                trimmed.insert(1, parts[i])
            else:
                trimmed.insert(1, "...")
                break

        self.sv_path.set(os.sep.join(trimmed))

    def set_slide(self, value: str):
        self.sv_slide.set(value)

    def set_max(self, value: str):
        self.slide_entry.config(to=int(value))
        self.sv_max.set(value)

    def reset_slide_info(self):
        self.slide_entry.config(to=1)
        self.sv_slide.set("")
        self.sv_max.set("")

    def on_browse(self):
        path = fd.askopenfilename(
            title="Select a PowerPoint file",
            filetypes=[("PowerPoint files", "*.pptx"), ("All files", "*.*")]
        )
        self.callbacks["change_path"](path)
    
    def on_export(self):
        path = fd.asksaveasfilename(
            title="Export PowerPoint Slide as Image",
            defaultextension=".jpg",
            filetypes=[
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )

        ext = os.path.splitext(path)[1]
        format = ext.strip(".").upper()
        
        self.callbacks["do_export"](path, format)
        
    def run(self):
        self.window.mainloop()