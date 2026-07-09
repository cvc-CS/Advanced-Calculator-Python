"""
ANDRE CALC — v2 (Futuristic HUD Edition)
A scientific calculator built with Python + tkinter.

Matches the HTML/JS version: sidebar menu (BASIC / SCI / MEM / LOG),
cyan HUD styling, DEG/RAD toggle, and a persistent calculation history
(saved to a local history.json file next to this script).
"""

import tkinter as tk
import json
import math
import os

# ---------------------------------------------------------------
# THEME
# ---------------------------------------------------------------
BG          = "#05070C"
PANEL       = "#0A0E18"
PANEL_2     = "#0D1220"
LINE        = "#1B2436"
CYAN        = "#4CF3FF"
CYAN_DIM    = "#123138"
VIOLET      = "#9B7CFF"
TEXT        = "#DCEFFF"
TEXT_DIM    = "#5A7290"
DANGER      = "#FF5C7A"
KEY_BG      = "#0F1524"
KEY_HOVER   = "#131A2C"

FONT_DISPLAY = ("Consolas", 40, "bold")
FONT_HIST    = ("Consolas", 11)
FONT_KEY     = ("Segoe UI", 14, "bold")
FONT_KEY_SM  = ("Consolas", 11)
FONT_NAV     = ("Segoe UI", 10, "bold")
FONT_BRAND   = ("Segoe UI", 11, "bold")

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "andrecalc_history.json")

# ---------------------------------------------------------------
# STATE
# ---------------------------------------------------------------
A = None
operator = None
B = None
memory_value = 0.0
angle_mode = "DEG"
history_entries = []


def load_history():
    global history_entries
    try:
        with open(HISTORY_FILE, "r") as f:
            history_entries = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history_entries = []


def save_history():
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history_entries, f)
    except OSError:
        pass  # fail silently, history just won't persist


def remove_zero_decimal(num):
    if num == int(num):
        return str(int(num))
    return str(round(num, 8))


def clear_all():
    global A, operator, B
    A = None
    operator = None
    B = None


def do_math(num_a, num_b, op):
    if op == "+":
        return num_a + num_b
    if op == "-":
        return num_a - num_b
    if op == "×":
        return num_a * num_b
    if op == "÷":
        return num_a / num_b
    if op == "xʸ":
        return num_a ** num_b


def to_radians(value):
    return math.radians(value) if angle_mode == "DEG" else value


# ---------------------------------------------------------------
# WINDOW
# ---------------------------------------------------------------
root = tk.Tk()
root.title("ANDRE.CALC")
root.configure(bg=BG)
root.resizable(False, False)

console = tk.Frame(root, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
console.pack(padx=16, pady=16)

# ---------------------------------------------------------------
# SIDEBAR MENU
# ---------------------------------------------------------------
sidebar = tk.Frame(console, bg=PANEL_2, width=100)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

brand = tk.Label(sidebar, text="ANDRE", font=FONT_BRAND, bg=PANEL_2, fg=CYAN)
brand.pack(pady=(16, 0))
brand_sub = tk.Label(sidebar, text="CALC // v2", font=("Consolas", 8), bg=PANEL_2, fg=TEXT_DIM)
brand_sub.pack(pady=(0, 18))

nav_buttons = {}
active_panel = tk.StringVar(value="basic")


def make_nav_button(parent, label, idx, key):
    frame = tk.Frame(parent, bg=PANEL_2, cursor="hand2")
    frame.pack(fill="x", pady=2)

    tick = tk.Frame(frame, bg=TEXT_DIM, width=3, height=3)
    inner = tk.Frame(frame, bg=PANEL_2)
    inner.pack(pady=6)

    idx_lbl = tk.Label(inner, text=idx, font=("Consolas", 8), bg=PANEL_2, fg=TEXT_DIM)
    idx_lbl.pack()
    text_lbl = tk.Label(inner, text=label, font=FONT_NAV, bg=PANEL_2, fg=TEXT_DIM)
    text_lbl.pack()

    def on_click(event=None):
        switch_panel(key)

    for widget in (frame, inner, idx_lbl, text_lbl):
        widget.bind("<Button-1>", on_click)

    nav_buttons[key] = (frame, idx_lbl, text_lbl)
    return frame


make_nav_button(sidebar, "BASIC", "01", "basic")
make_nav_button(sidebar, "SCI", "02", "sci")
make_nav_button(sidebar, "MEM", "03", "mem")
make_nav_button(sidebar, "LOG", "04", "hist")

# ---------------------------------------------------------------
# MAIN PANEL
# ---------------------------------------------------------------
main = tk.Frame(console, bg=PANEL)
main.pack(side="left", fill="both", expand=True)

# top bar
topbar = tk.Frame(main, bg=PANEL, highlightbackground=LINE, highlightthickness=0)
topbar.pack(fill="x")
tk.Frame(main, bg=LINE, height=1).pack(fill="x")

status = tk.Label(topbar, text="●  SYSTEM READY", font=("Consolas", 9), bg=PANEL, fg=CYAN)
status.pack(side="left", padx=14, pady=8)

mode_frame = tk.Frame(topbar, bg=PANEL_2, highlightbackground=LINE, highlightthickness=1)
mode_frame.pack(side="right", padx=14, pady=6)

mode_buttons = {}


def set_angle_mode(mode):
    global angle_mode
    angle_mode = mode
    for key, btn in mode_buttons.items():
        if key == mode:
            btn.configure(bg=CYAN_DIM, fg=CYAN)
        else:
            btn.configure(bg=PANEL_2, fg=TEXT_DIM)


for mode in ("DEG", "RAD"):
    b = tk.Label(mode_frame, text=mode, font=("Consolas", 9, "bold"), bg=PANEL_2, fg=TEXT_DIM,
                 padx=8, pady=3, cursor="hand2")
    b.pack(side="left")
    b.bind("<Button-1>", lambda e, m=mode: set_angle_mode(m))
    mode_buttons[mode] = b
set_angle_mode("DEG")

# screen
screen = tk.Frame(main, bg=PANEL)
screen.pack(fill="x", padx=20, pady=(14, 6))

history_line = tk.Label(screen, text="", font=FONT_HIST, bg=PANEL, fg=TEXT_DIM, anchor="e")
history_line.pack(fill="x")

display_var = tk.StringVar(value="0")
display = tk.Label(screen, textvariable=display_var, font=FONT_DISPLAY, bg=PANEL, fg=TEXT, anchor="e")
display.pack(fill="x", pady=(4, 10))

tk.Frame(main, bg=CYAN_DIM, height=1).pack(fill="x", padx=20)

# panel container (holds the 4 switchable views)
panel_container = tk.Frame(main, bg=PANEL)
panel_container.pack(fill="both", expand=True, padx=16, pady=14)

panels = {}


def make_key(parent, label, value, kind="normal", font=FONT_KEY):
    colors = {
        "normal": (KEY_BG, TEXT),
        "op": ("#16233A", CYAN),
        "top": (KEY_BG, VIOLET),
        "equals": (CYAN, "#04141A"),
        "mem": (KEY_BG, TEXT_DIM),
    }
    bg, fg = colors.get(kind, (KEY_BG, TEXT))
    btn = tk.Label(parent, text=label, font=font, bg=bg, fg=fg,
                    width=4, height=2, cursor="hand2",
                    highlightbackground=LINE, highlightthickness=1)

    def on_enter(e):
        btn.configure(bg=KEY_HOVER if kind not in ("equals",) else CYAN)

    def on_leave(e):
        btn.configure(bg=bg)

    def on_click(e):
        handle_input(value)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<Button-1>", on_click)
    return btn


# ---- BASIC panel ----
basic_panel = tk.Frame(panel_container, bg=PANEL)
panels["basic"] = basic_panel

basic_layout = [
    [("AC", "AC", "top"), ("+/-", "+/-", "top"), ("%", "%", "top"), ("÷", "÷", "op")],
    [("7", "7", "normal"), ("8", "8", "normal"), ("9", "9", "normal"), ("×", "×", "op")],
    [("4", "4", "normal"), ("5", "5", "normal"), ("6", "6", "normal"), ("−", "-", "op")],
    [("1", "1", "normal"), ("2", "2", "normal"), ("3", "3", "normal"), ("+", "+", "op")],
    [("0", "0", "normal"), (".", ".", "normal"), ("⌫", "⌫", "top"), ("=", "=", "equals")],
]
for r, row in enumerate(basic_layout):
    for c, (label, value, kind) in enumerate(row):
        make_key(basic_panel, label, value, kind).grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
for i in range(4):
    basic_panel.grid_columnconfigure(i, weight=1)

# ---- SCI panel ----
sci_panel = tk.Frame(panel_container, bg=PANEL)
panels["sci"] = sci_panel

sci_layout = [
    [("√", "√"), ("x²", "x²"), ("1/x", "1/x"), ("xʸ", "xʸ")],
    [("sin", "sin"), ("cos", "cos"), ("tan", "tan"), ("log", "log")],
    [("π", "π"), ("e", "e"), ("ln", "ln"), ("n!", "!")],
]
for r, row in enumerate(sci_layout):
    for c, (label, value) in enumerate(row):
        kind = "op" if value == "xʸ" else "normal"
        make_key(sci_panel, label, value, kind, font=FONT_KEY_SM).grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
for i in range(4):
    sci_panel.grid_columnconfigure(i, weight=1)

# ---- MEM panel ----
mem_panel = tk.Frame(panel_container, bg=PANEL)
panels["mem"] = mem_panel

mem_layout = [("MC", "MC"), ("MR", "MR"), ("M+", "M+"), ("M-", "M-")]
for c, (label, value) in enumerate(mem_layout):
    make_key(mem_panel, label, value, "mem", font=FONT_KEY_SM).grid(row=0, column=c, padx=4, pady=4, sticky="nsew")
for i in range(4):
    mem_panel.grid_columnconfigure(i, weight=1)

# ---- HIST panel ----
hist_panel = tk.Frame(panel_container, bg=PANEL)
panels["hist"] = hist_panel

hist_canvas = tk.Canvas(hist_panel, bg=PANEL, highlightthickness=0, height=220)
hist_scrollbar = tk.Scrollbar(hist_panel, orient="vertical", command=hist_canvas.yview)
hist_list_frame = tk.Frame(hist_canvas, bg=PANEL)

hist_list_frame.bind("<Configure>", lambda e: hist_canvas.configure(scrollregion=hist_canvas.bbox("all")))
hist_canvas.create_window((0, 0), window=hist_list_frame, anchor="nw", width=380)
hist_canvas.configure(yscrollcommand=hist_scrollbar.set)

hist_canvas.pack(side="top", fill="both", expand=True)
hist_scrollbar.pack_forget()  # keep it clean; scroll with mouse wheel instead


def on_mousewheel(event):
    hist_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


hist_canvas.bind_all("<MouseWheel>", on_mousewheel)


def render_history():
    for widget in hist_list_frame.winfo_children():
        widget.destroy()

    if not history_entries:
        tk.Label(hist_list_frame, text="NO ENTRIES LOGGED", font=("Consolas", 10),
                 bg=PANEL, fg=TEXT_DIM).pack(pady=30)
        return

    for entry in reversed(history_entries):
        item = tk.Frame(hist_list_frame, bg="#0D1220", highlightbackground=LINE, highlightthickness=1)
        item.pack(fill="x", pady=4)

        expr_lbl = tk.Label(item, text=entry["expr"], font=("Consolas", 9), bg="#0D1220", fg=TEXT_DIM, anchor="e")
        expr_lbl.pack(fill="x", padx=10, pady=(6, 0))
        res_lbl = tk.Label(item, text=entry["result"], font=("Consolas", 14, "bold"), bg="#0D1220", fg=CYAN, anchor="e")
        res_lbl.pack(fill="x", padx=10, pady=(0, 6))

        def on_click(e, result=entry["result"]):
            clear_all()
            display_var.set(result)
            history_line.configure(text="")

        for w in (item, expr_lbl, res_lbl):
            w.bind("<Button-1>", on_click)
            w.configure(cursor="hand2")


def add_history_entry(expr, result):
    history_entries.append({"expr": expr, "result": result})
    if len(history_entries) > 50:
        history_entries.pop(0)
    save_history()
    render_history()


def clear_history(event=None):
    history_entries.clear()
    save_history()
    render_history()


clear_btn = tk.Label(hist_panel, text="CLEAR LOG", font=("Consolas", 9, "bold"), bg=PANEL, fg=DANGER,
                      highlightbackground=LINE, highlightthickness=1, pady=8, cursor="hand2")
clear_btn.pack(fill="x", pady=(8, 0))
clear_btn.bind("<Button-1>", clear_history)


def switch_panel(key):
    active_panel.set(key)
    for name, panel in panels.items():
        panel.pack_forget()
    panels[key].pack(fill="both", expand=True)

    for name, (frame, idx_lbl, text_lbl) in nav_buttons.items():
        if name == key:
            idx_lbl.configure(fg=CYAN)
            text_lbl.configure(fg=CYAN)
        else:
            idx_lbl.configure(fg=TEXT_DIM)
            text_lbl.configure(fg=TEXT_DIM)


switch_panel("basic")


# ---------------------------------------------------------------
# CALCULATOR LOGIC
# ---------------------------------------------------------------
OPERATOR_SYMBOLS = ["÷", "×", "-", "+", "="]
TOP_SYMBOLS = ["AC", "+/-", "%"]
MEMORY_SYMBOLS = ["MC", "MR", "M+", "M-"]
ADVANCED_SYMBOLS = ["√", "x²", "1/x", "sin", "cos", "tan", "log", "ln", "π", "e", "!"]
TWO_NUMBER_SYMBOLS = ["xʸ"]


def flash_display():
    display.configure(fg=CYAN)
    root.after(150, lambda: display.configure(fg=TEXT))


def handle_input(value):
    global A, operator, B, memory_value

    if value in OPERATOR_SYMBOLS or value in TWO_NUMBER_SYMBOLS:
        if value == "=":
            if A is not None and operator is not None:
                B = float(display_var.get())
                num_a, num_b = float(A), B
                try:
                    if operator == "÷" and num_b == 0:
                        raise ZeroDivisionError
                    result = do_math(num_a, num_b, operator)
                    expr_text = f"{remove_zero_decimal(num_a)} {operator} {remove_zero_decimal(num_b)}"
                    history_line.configure(text=f"{expr_text} =")
                    result_str = remove_zero_decimal(result)
                    display_var.set(result_str)
                    add_history_entry(expr_text, result_str)
                    flash_display()
                except ZeroDivisionError:
                    display_var.set("ERR")
                    history_line.configure(text="")
                clear_all()
        else:
            if operator is not None and B is not None:
                num_a, num_b = float(A), float(display_var.get())
                try:
                    if operator == "÷" and num_b == 0:
                        raise ZeroDivisionError
                    display_var.set(remove_zero_decimal(do_math(num_a, num_b, operator)))
                except ZeroDivisionError:
                    display_var.set("ERR")
                    clear_all()
                    return
            A = display_var.get()
            display_var.set("0")
            B = "0"
            operator = value

    elif value in TOP_SYMBOLS:
        if value == "AC":
            clear_all()
            display_var.set("0")
            history_line.configure(text="")
        elif value == "+/-":
            display_var.set(remove_zero_decimal(float(display_var.get()) * -1))
        elif value == "%":
            display_var.set(remove_zero_decimal(float(display_var.get()) / 100))

    elif value in MEMORY_SYMBOLS:
        current = float(display_var.get())
        if value == "MC":
            memory_value = 0.0
        elif value == "MR":
            display_var.set(remove_zero_decimal(memory_value))
        elif value == "M+":
            memory_value += current
        elif value == "M-":
            memory_value -= current

    elif value in ADVANCED_SYMBOLS:
        current = float(display_var.get())
        try:
            if value == "√":
                if current < 0:
                    raise ValueError
                result = math.sqrt(current)
            elif value == "x²":
                result = current ** 2
            elif value == "1/x":
                if current == 0:
                    raise ZeroDivisionError
                result = 1 / current
            elif value == "sin":
                result = math.sin(to_radians(current))
            elif value == "cos":
                result = math.cos(to_radians(current))
            elif value == "tan":
                result = math.tan(to_radians(current))
            elif value == "log":
                if current <= 0:
                    raise ValueError
                result = math.log10(current)
            elif value == "ln":
                if current <= 0:
                    raise ValueError
                result = math.log(current)
            elif value == "π":
                result = math.pi
            elif value == "e":
                result = math.e
            elif value == "!":
                if current < 0 or current != int(current):
                    raise ValueError
                result = math.factorial(int(current))
            result_str = remove_zero_decimal(result)
            add_history_entry(f"{value}({remove_zero_decimal(current)})", result_str)
            display_var.set(result_str)
            flash_display()
        except (ValueError, ZeroDivisionError):
            display_var.set("ERR")

    elif value == "⌫":
        current = display_var.get()
        display_var.set("0" if len(current) <= 1 else current[:-1])

    else:  # digits / decimal
        if value == ".":
            if "." not in display_var.get():
                display_var.set(display_var.get() + ".")
        else:
            display_var.set(value if display_var.get() == "0" else display_var.get() + value)


# ---------------------------------------------------------------
# KEYBOARD SUPPORT
# ---------------------------------------------------------------
KEY_MAP = {
    "plus": "+", "minus": "-", "asterisk": "×", "slash": "÷",
    "Return": "=", "KP_Enter": "=", "BackSpace": "⌫", "Escape": "AC",
}


def on_key_press(event):
    if event.char and event.char.isdigit():
        handle_input(event.char)
    elif event.char == ".":
        handle_input(".")
    elif event.keysym in KEY_MAP:
        handle_input(KEY_MAP[event.keysym])


root.bind("<Key>", on_key_press)

# ---------------------------------------------------------------
# STARTUP
# ---------------------------------------------------------------
load_history()
render_history()

root.mainloop()
