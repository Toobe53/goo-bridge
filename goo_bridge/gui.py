# SPDX-License-Identifier: GPL-3.0-or-later
"""Minimal Tkinter shell for GOO Bridge.

The full tabbed interface is built by the GUI task.  Keeping this module
importable without tkinter lets the CLI run on servers and in Blender's
bundled Python, which has no Tk.
"""

from __future__ import annotations

import json
import os

BUTTONS = ["Doctor", "Analyze", "Render", "Close"]


def run_gui(argv: list[str] | None = None) -> int:
    try:
        import tkinter as tk
    except Exception as exc:  # pragma: no cover - platform dependent
        raise RuntimeError(f"Tkinter is not available: {exc}") from exc

    if os.environ.get("GOO_BRIDGE_SELFTEST") == "1":
        print(json.dumps({"ok": True, "buttons": BUTTONS, "opened": True}, ensure_ascii=True))
        return 0

    root = tk.Tk()
    root.title("GOO Bridge")
    root.geometry("860x560")
    header = tk.Label(root, text="GOO Bridge", font=("TkDefaultFont", 18, "bold"))
    header.pack(pady=12)
    tk.Label(root, text="Project, analyze, local/remote render, report.").pack()
    frame = tk.Frame(root)
    frame.pack(pady=20)
    for label in BUTTONS:
        tk.Button(frame, text=label, width=14, command=root.destroy if label == "Close" else lambda: None).pack(
            side=tk.LEFT, padx=4
        )
    root.mainloop()
    return 0
