import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import os
import threading
import subprocess

# ╔══════════════════════════════════════════════════════════╗
# ║              USER-CONFIGURABLE VARIABLES                 ║
# ╚══════════════════════════════════════════════════════════╝

# Paths to your VeraCrypt container files (.hc)
CONTAINER_PATH = r"D:\path\to\main\container.hc"
DECOY_PATH     = r"D:\path\to\decoy\container.hc"

# Drive letters to mount the volumes on
MAIN_DRIVE  = "X:"
DECOY_DRIVE = "Y:"

# Passwords for each volume
MAIN_PASS  = "actual password"
DECOY_PASS = "decoy password"

# Path to VeraCrypt executable
CRYPT_PATH = r"C:\Program Files\VeraCrypt\VeraCrypt.exe"

# Key combo to trigger the password prompt (entered as calculator presses)
# Default: 1 2 3 4 5 6
COMBO_KEYS = ['1', '2', '3', '4', '5', '6']

# ╔══════════════════════════════════════════════════════════╗
# ║                    THEME / COLORS                        ║
# ╚══════════════════════════════════════════════════════════╝

BG          = "#1c1c27"
DISPLAY_BG  = "#0f0f18"
BTN_NUM     = "#2a2a3d"
BTN_OP      = "#3d3452"
BTN_EQ      = "#7c6fcd"
BTN_CLR     = "#5c3a4a"
FG          = "#e0d9f7"
FG_DARK     = "#1c1c27"
FG_DIM      = "#8880aa"
HOVER_NUM   = "#3a3a52"
HOVER_OP    = "#524870"
HOVER_EQ    = "#9d8fe8"
HOVER_CLR   = "#7a4d5e"

FONT_DISPLAY = ("Consolas", 28, "bold")
FONT_SUBTEXT = ("Consolas", 11)
FONT_BTN     = ("Consolas", 15, "bold")
FONT_BTN_SM  = ("Consolas", 13)

# ══════════════════════════════════════════════════════════


def crypt_exists():
    if not os.path.exists(CRYPT_PATH):
        tk.messagebox.showerror(
            "VeraCrypt Missing",
            f"VeraCrypt executable not found at:\n{CRYPT_PATH}\n\nUpdate CRYPT_PATH in the script."
        )
        return False
    return True


def mount_vol(path, drive, pwd):
    if not crypt_exists():
        return False, "VeraCrypt not found"
    args = [CRYPT_PATH, '/v', path, '/l', drive[0], '/p', pwd, '/q']
    try:
        subprocess.run(
            args, capture_output=True, text=True,
            check=True, encoding='utf-8', errors='ignore'
        )
        return True, f"Mounted {path} → {drive}"
    except subprocess.CalledProcessError as e:
        return False, f"Mount failed (code {e.returncode})"
    except Exception as e:
        return False, f"Unexpected error: {e}"


# ── Hover effect helpers ──────────────────────────────────

def on_enter(btn, color):
    btn.configure(bg=color)

def on_leave(btn, color):
    btn.configure(bg=color)


class Calculator:
    def __init__(self, win):
        self.win = win
        win.title("Calculator")
        win.geometry("360x580")
        win.resizable(False, False)
        win.configure(bg=BG)

        self.expr          = ""
        self.combo         = []
        self.just_evaluated = False

        self.display_main = tk.StringVar(value="0")
        self.display_sub  = tk.StringVar(value="")

        self._build_display()
        self._build_buttons()
        self._bind_keys()

    # ── UI construction ───────────────────────────────────

    def _build_display(self):
        frame = tk.Frame(self.win, bg=DISPLAY_BG, pady=8)
        frame.pack(fill="x", padx=12, pady=(12, 6))

        self.sub_label = tk.Label(
            frame, textvariable=self.display_sub,
            font=FONT_SUBTEXT, bg=DISPLAY_BG, fg=FG_DIM,
            anchor="e", padx=14
        )
        self.sub_label.pack(fill="x")

        self.main_label = tk.Label(
            frame, textvariable=self.display_main,
            font=FONT_DISPLAY, bg=DISPLAY_BG, fg=FG,
            anchor="e", padx=14, height=2
        )
        self.main_label.pack(fill="x")

    def _build_buttons(self):
        frame = tk.Frame(self.win, bg=BG)
        frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # (label, bg_color, hover_color, colspan)
        layout = [
            [("AC", BTN_CLR, HOVER_CLR), ("C",  BTN_CLR, HOVER_CLR),
             ("%",  BTN_OP,  HOVER_OP),  ("/",  BTN_OP,  HOVER_OP)],

            [("7",  BTN_NUM, HOVER_NUM), ("8",  BTN_NUM, HOVER_NUM),
             ("9",  BTN_NUM, HOVER_NUM), ("*",  BTN_OP,  HOVER_OP)],

            [("4",  BTN_NUM, HOVER_NUM), ("5",  BTN_NUM, HOVER_NUM),
             ("6",  BTN_NUM, HOVER_NUM), ("-",  BTN_OP,  HOVER_OP)],

            [("1",  BTN_NUM, HOVER_NUM), ("2",  BTN_NUM, HOVER_NUM),
             ("3",  BTN_NUM, HOVER_NUM), ("+",  BTN_OP,  HOVER_OP)],

            # last row: "0" spans 2 cols
            [("0",  BTN_NUM, HOVER_NUM, 2), (".",  BTN_NUM, HOVER_NUM),
             ("=",  BTN_EQ,  HOVER_EQ)],
        ]

        for r, row in enumerate(layout):
            col = 0
            for item in row:
                txt    = item[0]
                bg     = item[1]
                hover  = item[2]
                span   = item[3] if len(item) > 3 else 1
                fg     = FG_DARK if txt == "=" else FG

                btn = tk.Button(
                    frame, text=txt, font=FONT_BTN if len(txt) <= 2 else FONT_BTN_SM,
                    bg=bg, fg=fg, activebackground=hover,
                    activeforeground=fg, bd=0, relief="flat",
                    cursor="hand2",
                    command=lambda x=txt: self.click(x)
                )
                btn.grid(row=r, column=col, columnspan=span,
                         padx=3, pady=3, sticky="nsew")

                btn.bind("<Enter>", lambda e, b=btn, h=hover: on_enter(b, h))
                btn.bind("<Leave>", lambda e, b=btn, orig=bg: on_leave(b, orig))

                col += span

        for i in range(len(layout)):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)

    def _bind_keys(self):
        self.win.bind('<Return>',    lambda e: self.click('='))
        self.win.bind('<BackSpace>', lambda e: self.click('C'))
        self.win.bind('<Escape>',    lambda e: self.click('AC'))
        self.win.bind('<Key>',       self._handle_key)

    # ── Key / click logic ─────────────────────────────────

    def _handle_key(self, event):
        k = event.char
        if k in '0123456789':
            self.click(k)
        elif k in '.+-*/':
            self.click(k)
        elif k == '\r':
            self.click('=')

    def click(self, ch):
        # ── Combo tracking ───────────────────────────────
        self.combo.append(ch)
        if len(self.combo) > len(COMBO_KEYS):
            self.combo.pop(0)
        if self.combo == COMBO_KEYS:
            self.combo = []
            self.expr  = ""
            self.display_main.set("• • •")
            self.display_sub.set("")
            self.win.update()
            self._ask_pass()
            return

        # ── Calculator logic ──────────────────────────────
        if ch == 'AC':
            self.expr           = ""
            self.just_evaluated = False
            self.combo          = []
            self.display_main.set("0")
            self.display_sub.set("")

        elif ch == 'C':
            self.expr = self.expr[:-1]
            self.display_main.set(self.expr or "0")
            self.display_sub.set("")

        elif ch == '=':
            if not self.expr:
                return
            try:
                result = eval(self.expr)
                # clean up float trailing zeros
                result_str = (
                    str(int(result))
                    if isinstance(result, float) and result.is_integer()
                    else str(result)
                )
                self.display_sub.set(self.expr + " =")
                self.display_main.set(result_str)
                self.expr           = result_str
                self.just_evaluated = True
            except Exception:
                self.display_main.set("Error")
                self.display_sub.set("")
                self.expr = ""

        elif ch == '%':
            if not self.expr:
                return
            try:
                result = eval(self.expr) / 100
                result_str = (
                    str(int(result))
                    if isinstance(result, float) and result.is_integer()
                    else str(result)
                )
                self.display_sub.set(self.expr + " %")
                self.display_main.set(result_str)
                self.expr           = result_str
                self.just_evaluated = True
            except Exception:
                self.display_main.set("Error")
                self.expr = ""

        elif ch in '+-*/':
            self.just_evaluated = False
            if not self.expr:
                # allow starting with minus for negatives
                if ch == '-':
                    self.expr = '-'
                    self.display_main.set(self.expr)
                return
            # replace trailing operator instead of stacking
            if self.expr[-1] in '+-*/':
                self.expr = self.expr[:-1] + ch
            else:
                self.expr += ch
            self.display_main.set(self.expr)
            self.display_sub.set("")

        elif ch == '.':
            self.just_evaluated = False
            # get the last number token
            import re
            tokens = re.split(r'[+\-*/]', self.expr)
            last   = tokens[-1] if tokens else ""
            if '.' not in last:
                self.expr += ('0.' if not last else '.')
                self.display_main.set(self.expr)

        else:  # digit
            if self.just_evaluated:
                # fresh start after evaluation
                self.expr           = ch
                self.just_evaluated = False
            elif not self.expr or self.display_main.get() == "0":
                self.expr = ch
            else:
                self.expr += ch
            self.display_main.set(self.expr)

    # ── Mount / auth ──────────────────────────────────────

    def _ask_pass(self):
        if not crypt_exists():
            self.display_main.set("0")
            return

        pwd = tkinter.simpledialog.askstring(
            "Authentication", "Enter Access Key:", show='*',
            parent=self.win
        )

        if pwd is None:
            self.display_main.set("0")
            self.display_sub.set("")
            return

        def bg_mount(container, drive, p):
            ok, msg = mount_vol(container, drive, p)
            print(f"[mount] {msg}")

        if pwd == MAIN_PASS:
            self.display_main.set("Granted")
            self.display_sub.set("mounting...")
            t = threading.Thread(
                target=bg_mount,
                args=(CONTAINER_PATH, MAIN_DRIVE, pwd),
                daemon=True
            )
            t.start()

        elif pwd == DECOY_PASS:
            self.display_main.set("Granted")
            self.display_sub.set("mounting...")
            t = threading.Thread(
                target=bg_mount,
                args=(DECOY_PATH, DECOY_DRIVE, pwd),
                daemon=True
            )
            t.start()

        else:
            self.display_main.set("0")
            self.display_sub.set("")
            tk.messagebox.showwarning("Access Denied", "Incorrect password.", parent=self.win)


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()