import tkinter
import math

# ============================================================
# BUTTON LAYOUT
# ============================================================
button_values = [
    ["MC", "MR", "M+", "M-"],
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "⌫", "="],
    ["√", "x²", "1/x", "xʸ"],
    ["sin", "cos", "tan", "log"],
    ["π", "e", "ln", "!"]
]

right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%"]
memory_symbols = ["MC", "MR", "M+", "M-"]
advanced_symbols = ["√", "x²", "1/x", "sin", "cos", "tan", "log", "ln", "π", "e", "!"]
two_number_symbols = ["xʸ"]

row_count = len(button_values)
column_count = len(button_values[0])

# ---------------- COLOR PALETTE ----------------
color_bg = "#0F0F14"
color_text_main = "#FFFFFF"
color_text_history = "#6B6B76"
color_num_bg = "#2B2B33"
color_num_bg_hover = "#38383F"     # NEW - lighter shade on hover
color_top_bg = "#3F3F49"
color_top_bg_hover = "#4C4C57"
color_operator_bg = "#FF9F0A"
color_operator_bg_hover = "#FFB238"
color_operator_text = "#FFFFFF"
color_memory_bg = "#2C3E50"
color_memory_bg_hover = "#37516A"
color_sci_bg = "#232329"
color_sci_bg_hover = "#2E2E36"
color_sci_text = "#B8B8C2"
color_brand = "#FF9F0A"

FONT_FAMILY = "Helvetica Neue"

BUTTON_WIDTH = 6   # NEW - wider buttons since window is wider now

# window setup
window = tkinter.Tk()
window.title("Calculator")
window.configure(bg=color_bg)
window.resizable(False, False)

outer_frame = tkinter.Frame(window, bg=color_bg, padx=20, pady=16)
outer_frame.pack()

# ---------------- BRANDING (NEW) ----------------
brand_frame = tkinter.Frame(outer_frame, bg=color_bg)
brand_frame.pack(fill="x", pady=(0, 10))

brand_label = tkinter.Label(brand_frame, text="ANDRE", font=(FONT_FAMILY, 13, "bold"),
                             bg=color_bg, fg=color_brand, anchor="w")
brand_label.pack(side="left")

brand_sub_label = tkinter.Label(brand_frame, text=" CALC", font=(FONT_FAMILY, 13),
                                 bg=color_bg, fg=color_text_history, anchor="w")
brand_sub_label.pack(side="left")

frame = tkinter.Frame(outer_frame, bg=color_bg)
frame.pack()

history_label = tkinter.Label(frame, text="", font=(FONT_FAMILY, 14),
                               background=color_bg, foreground=color_text_history,
                               anchor="e", width=column_count * (BUTTON_WIDTH - 2), padx=10)
history_label.grid(row=0, column=0, columnspan=column_count, sticky="we", pady=(0, 4))

label = tkinter.Label(frame, text="0", font=(FONT_FAMILY, 48, "bold"),
                       background=color_bg, foreground=color_text_main,
                       anchor="e", width=column_count * (BUTTON_WIDTH - 2), padx=10)
label.grid(row=1, column=0, columnspan=column_count, sticky="we", pady=(0, 14))


def get_button_colors(value):
    if value in memory_symbols:
        return color_memory_bg, color_memory_bg_hover, "#FFFFFF"
    elif value in top_symbols:
        return color_top_bg, color_top_bg_hover, "#FFFFFF"
    elif value in right_symbols or value in two_number_symbols:
        return color_operator_bg, color_operator_bg_hover, color_operator_text
    elif value in advanced_symbols:
        return color_sci_bg, color_sci_bg_hover, color_sci_text
    else:
        return color_num_bg, color_num_bg_hover, "#FFFFFF"


# NEW: micro-interaction handlers - button lightens on hover, darkens on click
def on_enter(event, hover_color):
    event.widget["background"] = hover_color


def on_leave(event, normal_color):
    event.widget["background"] = normal_color


def on_press(event, press_color):
    event.widget["background"] = press_color


buttons_grid = {}

for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        if value == "":
            continue

        bg_color, hover_color, fg_color = get_button_colors(value)

        if value in advanced_symbols or value in memory_symbols:
            btn_font = (FONT_FAMILY, 15)
        else:
            btn_font = (FONT_FAMILY, 22)

        button = tkinter.Button(frame, text=value, font=btn_font,
                                 width=BUTTON_WIDTH, height=2,
                                 bg=bg_color, fg=fg_color,
                                 activebackground=hover_color, activeforeground=fg_color,
                                 relief="flat", bd=0, cursor="hand2",
                                 highlightthickness=0,
                                 command=lambda value=value: button_clicked(value))

        # NEW: buttons touch each other - no padx/pady, no gaps
        button.grid(row=row + 2, column=column, padx=0, pady=0, sticky="nsew")

        # NEW: micro-interactions - hover lightens, press flashes brighter
        button.bind("<Enter>", lambda e, h=hover_color: on_enter(e, h))
        button.bind("<Leave>", lambda e, c=bg_color: on_leave(e, c))
        button.bind("<ButtonPress-1>", lambda e, h=hover_color: on_press(e, h))

        buttons_grid[(row, column)] = button

frame.pack()

# ============================================================
# CALCULATOR "MEMORY"
# ============================================================
A = 0
operator = None
B = None
memory_value = 0


def remove_zero_decimal(num):
    if num % 1 == 0:
        num = int(num)
        return str(num)
    return str(round(num, 8))


def clear_all():
    global A, B, operator
    A = 0
    B = None
    operator = None


def do_math(numA, numB, op):
    if op == "+":
        return numA + numB
    elif op == "-":
        return numA - numB
    elif op == "×":
        return numA * numB
    elif op == "÷":
        return numA / numB
    elif op == "xʸ":
        return numA ** numB


def button_clicked(value):
    global right_symbols, top_symbols, label, A, B, operator, memory_value

    if value in right_symbols or value in two_number_symbols:
        if value == "=":
            if A is not None and operator is not None:
                B = float(label["text"])
                numA = float(A)
                numB = float(B)
                try:
                    result = do_math(numA, numB, operator)
                    history_label["text"] = f"{remove_zero_decimal(numA)} {operator} {remove_zero_decimal(numB)} ="
                    label["text"] = remove_zero_decimal(result)
                except ZeroDivisionError:
                    label["text"] = "Error"
                    history_label["text"] = ""
                clear_all()
        else:
            if operator is not None and B is not None:
                numA = float(A)
                numB = float(label["text"])
                try:
                    result = do_math(numA, numB, operator)
                    label["text"] = remove_zero_decimal(result)
                except ZeroDivisionError:
                    label["text"] = "Error"
                    clear_all()
                    return

            A = label["text"]
            label["text"] = "0"
            B = "0"
            operator = value

    elif value in top_symbols:
        if value == "AC":
            clear_all()
            label["text"] = "0"
            history_label["text"] = ""
        elif value == "+/-":
            result = float(label["text"]) * -1
            label["text"] = remove_zero_decimal(result)
        elif value == "%":
            result = float(label["text"]) / 100
            label["text"] = remove_zero_decimal(result)

    elif value in memory_symbols:
        current = float(label["text"])
        if value == "MC":
            memory_value = 0
        elif value == "MR":
            label["text"] = remove_zero_decimal(memory_value)
        elif value == "M+":
            memory_value += current
        elif value == "M-":
            memory_value -= current

    elif value in advanced_symbols:
        try:
            current = float(label["text"])
            if value == "√":
                label["text"] = "Error" if current < 0 else remove_zero_decimal(current ** 0.5)
            elif value == "x²":
                label["text"] = remove_zero_decimal(current ** 2)
            elif value == "1/x":
                label["text"] = remove_zero_decimal(1 / current)
            elif value == "sin":
                label["text"] = remove_zero_decimal(math.sin(math.radians(current)))
            elif value == "cos":
                label["text"] = remove_zero_decimal(math.cos(math.radians(current)))
            elif value == "tan":
                label["text"] = remove_zero_decimal(math.tan(math.radians(current)))
            elif value == "log":
                label["text"] = "Error" if current <= 0 else remove_zero_decimal(math.log10(current))
            elif value == "ln":
                label["text"] = "Error" if current <= 0 else remove_zero_decimal(math.log(current))
            elif value == "π":
                label["text"] = remove_zero_decimal(math.pi)
            elif value == "e":
                label["text"] = remove_zero_decimal(math.e)
            elif value == "!":
                if current < 0 or current % 1 != 0:
                    label["text"] = "Error"
                else:
                    label["text"] = remove_zero_decimal(math.factorial(int(current)))
        except (ZeroDivisionError, ValueError):
            label["text"] = "Error"

    elif value == "⌫":
        current_text = label["text"]
        label["text"] = "0" if len(current_text) <= 1 else current_text[:-1]

    else:
        if value == ".":
            if value not in label["text"]:
                label["text"] += value
        elif value in "0123456789":
            if label["text"] == "0":
                label["text"] = value
            else:
                label["text"] += value


# ============================================================
# KEYBOARD SUPPORT
# ============================================================
key_map = {
    "+": "+", "-": "-", "*": "×", "/": "÷",
    "\r": "=", "\x08": "⌫",
}


def key_pressed(event):
    char = event.char
    if char in "0123456789.":
        button_clicked(char)
    elif char in key_map:
        button_clicked(key_map[char])


window.bind("<Key>", key_pressed)

# center the window on the screen
window.update_idletasks()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.mainloop()