import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import tkinter.font as tkfont

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

def is_dark_mode():
    # Check if Windows is using dark mode
    try:
        key = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as reg_key:
            value, _ = winreg.QueryValueEx(reg_key, "AppsUseLightTheme")
        return value == 0  # 0 means dark mode
    except Exception:
        return False  # Default to light mode if detection fails

def new_file(event = None):
    text_area.delete("1.0", tk.END)

def open_file(event = None):
    filepath = filedialog.askopenfilename(
        filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
    )

    if filepath:
        with open(filepath, "r") as file:
            content = file.read()
            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", content)

def save_file(event = None):
    pass

def close_file(event = None):
    window.destroy()

def get_Theme():
    return "dark" if is_dark_mode() else "light"

colours = {
    "dark": {
        "bg": "#2e2e2e",
        "fg": "#ffffff",
        "button_bg": "#444444",
        "button_fg": "#ffffff",
    },
    "light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "button_bg": "#dddddd",
        "button_fg": "#000000",
    },
}

def change_font(event = None):
    getFont = font_combobox.get()
    getSize = size_combobox.get()
    if getSize.isdigit():
        text_area.config(font = (getFont, getSize))
        font_window.destroy()

def open_fontWindow(event = None):
    global font_window, font_combobox, size_combobox

    font_window = tk.Toplevel(window)
    font_window.title("Select font")
    font_window.geometry("300x300")

    current_font = text_area.cget("font")
    current_font = tkfont.Font(font = current_font)
    cfont = current_font.actual("family")
    csize = current_font.actual("size")

    #making the font selection dropdown menu
    tk.Label(font_window, text = "Font: ").pack(pady=5)
    available_fonts = [font for font in tkfont.families()]
    font_combobox = ttk.Combobox(font_window, values = available_fonts, state = "readonly")
    font_combobox.set(cfont)
    font_combobox.pack(pady = 5)

    #making the font size selection dropdown
    tk.Label(font_window, text = "Size: ").pack(pady = 5)
    available_sizes = ['8', '9', '10', '11', '12', '14', '16', '18', '20', '22', '24', '26', '28', '36', '48', '72']
    size_combobox = ttk.Combobox(font_window, values = available_sizes)
    size_combobox.set(csize)
    size_combobox.pack(pady = 5)

    apply_button = tk.Button(font_window, text = "Apply", command = change_font)
    apply_button.pack(pady = 15)

def change_theme(theme):
    window.config(bg = colours[theme]["bg"])
    text_area.config(bg = colours[theme]["bg"], fg = colours[theme]["fg"])

def toggle_wordWrap(event = None):
    if (text_area.cget("wrap") == "none"):
        text_area.config(wrap = "word")
        view_menu.entryconfig(0, label = "Word Wrap    √")
    else:
        text_area.config(wrap = "none")
        view_menu.entryconfig(0, label = "Word Wrap    X")

def toggle_darkMode(event = None):
    global current_theme
    if (current_theme == "dark"):
        current_theme = "light"
        change_theme("light")
        view_menu.entryconfig(1, label = "Dark Mode    X")
    else:
        current_theme = "dark"
        change_theme("dark")
        view_menu.entryconfig(1, label = "Dark Mode    √")

window = tk.Tk()
window.title("Notepad X")
window.geometry("800x600")

text_area = tk.Text(window,undo = True, wrap = "word", font = ("Consolas", 16))
text_area.pack(expand = 1, fill = "both")


menu_bar = tk.Menu(window)

file_menu = tk.Menu(menu_bar, tearoff = 0)
file_menu.add_command(label="New     Ctrl + N", command=new_file)
file_menu.add_command(label="Open    Ctrl + O", command=open_file)
file_menu.add_command(label="Save    Ctrl + S", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit    Ctrl + W", command=close_file)

edit_menu = tk.Menu(menu_bar, tearoff = 0)
edit_menu.add_command(label = "Undo    Ctrl + Z", command = text_area.edit_undo)
edit_menu.add_command(label = "Redo    Ctrl + Y", command = text_area.edit_redo)
edit_menu.add_separator()
edit_menu.add_command(label = "Copy    Ctrl + C", command = lambda: text_area.event_generate("<Control-c>"))
edit_menu.add_command(label = "Cut       Ctrl + X", command = lambda: text_area.event_generate("<Control-x>"))
edit_menu.add_command(label = "Paste    Ctrl + V", command = lambda: text_area.event_generate("<Control-v>"))
edit_menu.add_separator()
edit_menu.add_command(label = "Font     Ctrl + F", command = open_fontWindow)

view_menu = tk.Menu(menu_bar, tearoff = 0)
view_menu.add_command(label = "Word Wrap    √", command = toggle_wordWrap)
view_menu.add_command(label = "Dark Mode    √", command = toggle_darkMode)

menu_bar.add_cascade(label = "File", menu = file_menu)
menu_bar.add_cascade(label = "Edit", menu = edit_menu)
menu_bar.add_cascade(label = "Settings", menu = view_menu)

window.config(menu = menu_bar)

window.bind("<Control-n>", new_file)
window.bind("<Control-o>", open_file)
window.bind("<Control-s>", save_file)
window.bind("<Control-w>", close_file)
window.bind("<Control-f>", open_fontWindow)

text_area.bind("<Control-z>", lambda event: text_area.edit_undo)
text_area.bind("<Control-y>", lambda event: text_area.edit_redo)

current_theme = get_Theme()
change_theme(current_theme)

window.iconbitmap('icon.ico')

window.mainloop()