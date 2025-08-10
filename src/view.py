import tkinter as tk
from tkinter import ttk
from typing import Callable


class View(object):

    def __init__(self):
        self.callbacks = {}
        self.window = tk.Tk()

        self.sv_path = tk.StringVar(self.window, "")
        self.sv_slide = tk.StringVar(self.window, "")
        self.sv_max = tk.StringVar(self.window, "")


        self._show()


    def _show(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        frame.columnconfigure(0, weight=9)

        browse_frame = tk.Frame(frame)
        browse_frame.grid(column=0, row=0, sticky="NSEW", pady=4)
        browse_frame.columnconfigure(0, weight=9)

        browse_label = tk.Label(browse_frame, relief="groove", textvariable=self.sv_path)
        browse_label.grid(column=0, row=0, sticky="NSEW", padx=4)
        
        browse_button = tk.Button(browse_frame, width=80, text="Browse", command=self.on_browse)
        browse_button.grid(column=1, row=9, sticky="NSEW", padx=4)

        param_frame = tk.Frame(frame)
        param_frame.grid(column=0, row=1, sticky="NSEW", pady=4)

        slide_frame = ttk.Labelframe(param_frame, text="Slide")
        slide_frame.grid(column=0, row=0, sticky="NSEW", padx=4)

        slide_entry = ttk.Spinbox(slide_frame, width=5, from_=1, textvariable=self.sv_slide)
        slide_entry.grid(column=0, row=0, sticky="NSEW", padx=4)

        tk.Label(slide_frame, text="/").grid(column=1, row=0, sticky="NSEW", padx=4)

        max_label = tk.Label(slide_frame, width=5, relief="groove", textvariable=self.sv_max)
        max_label.grid(column=2, row=0, sticky="NSEW", padx=4)


        buttons_frame = tk.Frame(frame)
        buttons_frame.grid(column=0, row=2, sticky="NSEW", pady=4)

        self.export_button = tk.Button(buttons_frame, text="Export", command=self.on_export)
        self.export_button.grid(column=0, row=0, sticky="NSEW", padx=20)

    def add_callbacks(self, callbacks: dict[str, Callable]):
        for key, callback in callbacks.items():
            self.callbacks[key] = callback

    def bind_callbacks(self):
        def slide_trace(*_):
            value = self.sv_slide.get()
            if "change_slide" in self.callbacks:
                self.callbacks["change_slide"](value)

        self.sv_slide.trace_add("write", slide_trace)

    def set_slide(self, value: str):
        self.sv_slide.set(value)

    def on_browse(self):
        pass

    
    def on_export(self):
        pass

    def run(self):
        self.window.mainloop()