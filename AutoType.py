# python code for auto typing
import pyautogui
import time
import random
import threading
from tkinter import *
from tkinter import ttk

# Allow the mouse to be moved freely (e.g. to click where you want to type)
# without triggering pyautogui's failsafe abort.
pyautogui.FAILSAFE = False

# ---------- palette (soft, low-glare light theme) ----------
BG = "#e7e9f0"
CARD = "#f4f5f9"
BORDER = "#d5d7e1"
TEXT_COLOR = "#2b2c36"
MUTED = "#6e7080"
ACCENT = "#5169d6"
ACCENT_HOVER = "#4257bd"
FIELD_BG = "#e3e5ee"

root = Tk()
root.title("Auto Type")
root.geometry("480x620+155+60")
root.minsize(480, 800)
root.config(bg=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("Accent.Horizontal.TScale", background=BG, troughcolor=FIELD_BG)


def card(parent, **kw):
    return Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1, **kw)


# ---------- header ----------
header = Frame(root, bg=BG)
header.pack(fill="x", padx=26, pady=(18, 8))

Label(header, text="Auto Type", font=("Segoe UI", 19, "bold"),
      bg=BG, fg=TEXT_COLOR).pack(anchor="w")
Label(header, text="Type out text automatically, after a delay you set.",
      font=("Segoe UI", 10), bg=BG, fg=MUTED).pack(anchor="w", pady=(2, 0))

# ---------- text card ----------
text_card = card(root)
text_card.pack(fill="both", expand=True, padx=26, pady=8)

Label(text_card, text="TEXT", font=("Segoe UI", 9, "bold"),
      bg=CARD, fg=MUTED).pack(anchor="w", padx=16, pady=(14, 6))

text_wrap = Frame(text_card, bg=CARD)
text_wrap.pack(fill="both", expand=True, padx=16, pady=(0, 14))

scrollbar = Scrollbar(text_wrap)
scrollbar.pack(side="right", fill="y")

e = Text(text_wrap, width=60, height=7, bg=FIELD_BG, fg=TEXT_COLOR,
         insertbackground=TEXT_COLOR, font=("Consolas", 11),
         relief="flat", padx=10, pady=10, wrap="word",
         yscrollcommand=scrollbar.set)
e.pack(side="left", fill="both", expand=True)
scrollbar.config(command=e.yview)

# ---------- settings card ----------
settings_card = card(root)
settings_card.pack(fill="x", padx=26, pady=8)

settings_inner = Frame(settings_card, bg=CARD)
settings_inner.pack(fill="x", padx=16, pady=10)

# delay row
delay_row = Frame(settings_inner, bg=CARD)
delay_row.pack(fill="x", pady=(0, 12))
Label(delay_row, text="Start after", font=("Segoe UI", 11), bg=CARD, fg=TEXT_COLOR).pack(side="left")
Label(delay_row, text="seconds", font=("Segoe UI", 9), bg=CARD, fg=MUTED).pack(side="right")
s = Entry(delay_row, width=5, bg=FIELD_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
          font=("Segoe UI", 12), relief="flat", justify="center")
s.pack(side="right", padx=(0, 8), ipady=4)
s.insert(0, 5)

# speed row
speed_row = Frame(settings_inner, bg=CARD)
speed_row.pack(fill="x")
Label(speed_row, text="Typing speed", font=("Segoe UI", 11), bg=CARD, fg=TEXT_COLOR).pack(side="left")

# --- Human like checkbox (kept small, tucked into the speed row so it
# doesn't add a new row / grow the window) ---
human_like_var = BooleanVar(value=False)
human_like_chk = Checkbutton(
    speed_row, text="Human like", variable=human_like_var,
    font=("Segoe UI", 8), bg=CARD, fg=MUTED,
    activebackground=CARD, activeforeground=TEXT_COLOR,
    selectcolor=FIELD_BG, bd=0, highlightthickness=0,
    cursor="hand2", padx=0
)
human_like_chk.pack(side="right")

style.configure("Modern.Horizontal.TScale",
                troughcolor=FIELD_BG,
                background=ACCENT,
                sliderrelief="flat",
                sliderlength=14)

x = ttk.Scale(settings_inner, from_=1, to=10, orient="horizontal",
              length=380, style="Modern.Horizontal.TScale")
x.set(10)
x.pack(fill="x", pady=(6, 0))


speed_labels = Frame(settings_inner, bg=CARD)
speed_labels.pack(fill="x")

Label(speed_labels, text="slow", font=("Segoe UI", 8),
      bg=CARD, fg=MUTED).pack(side="left")

Label(speed_labels, text="fast", font=("Segoe UI", 8),
      bg=CARD, fg=MUTED).pack(side="right")


# s is sleep
# x is speed
# human_like: bool - adds random pauses + backspace/retype "mistakes"

stop_event = threading.Event()


def interruptible_sleep(seconds):
    """Sleep in small steps so Cancel/Esc stays responsive. Returns False if
    the stop event fired while waiting."""
    waited = 0.0
    while waited < seconds:
        if stop_event.is_set():
            return False
        step = min(0.15, seconds - waited)
        time.sleep(step)
        waited += step
    return True


def do_typing(s, x, human_like):
    try:
        if s == "":
            s = 5
        if not interruptible_sleep(int(s)):
            return

        text = e.get(1.0, END)
        xx = ((11 - float(x)) / 100)

        CHUNK_SIZE = 8
        for i in range(0, len(text), CHUNK_SIZE):
            if stop_event.is_set():
                return
            chunk = text[i:i + CHUNK_SIZE]
            pyautogui.typewrite(chunk, interval=xx)

            if human_like:
                # occasionally backspace the tail of what was just typed,
                # then retype it (simulated "mistake")
                if chunk.strip() and random.random() < 0.2:
                    backspace_count = random.randint(1, min(3, len(chunk)))
                    retyped = chunk[-backspace_count:]

                    if not interruptible_sleep(random.uniform(0.2, 0.6)):
                        return
                    for _ in range(backspace_count):
                        if stop_event.is_set():
                            return
                        pyautogui.press('backspace')
                        time.sleep(random.uniform(0.05, 0.15))
                    if not interruptible_sleep(random.uniform(0.2, 0.5)):
                        return
                    pyautogui.typewrite(retyped, interval=xx)

                # random pause between typing chunks
                if random.random() < 0.3:
                    if not interruptible_sleep(random.uniform(1, 10)):
                        return
    finally:
        root.after(0, reset_buttons)


def typei(s, x):
    stop_event.clear()
    start_typing.config(state="disabled", bg="#b9bfe0", cursor="arrow")
    cancel_btn.config(state="normal", cursor="hand2")
    threading.Thread(
        target=do_typing,
        args=(s, x, human_like_var.get()),
        daemon=True
    ).start()


def stop_typing(event=None):
    stop_event.set()


def reset_buttons():
    start_typing.config(state="normal", bg=ACCENT, cursor="hand2")
    cancel_btn.config(state="disabled", cursor="arrow")


def shift_line_to_left(s):
    arr = s.splitlines()
    ans = ""
    for i in arr:
        ans = ans + i.strip() + "\n"
    e.delete(1.0, END)
    e.insert(1.0, ans)


# ---------- buttons ----------
btn_frame = Frame(root, bg=BG)
btn_frame.pack(fill="x", padx=26, pady=(8, 18))


def pointerInside(ev):
    ev.widget['background'] = "#e6e8f0"


def pointerOutside(ev):
    ev.widget['background'] = CARD


leftShift = Button(btn_frame, text="Remove indentation", activebackground="#e6e8f0",
                    activeforeground=TEXT_COLOR,
                    font=("Segoe UI", 11), bg=CARD, fg=TEXT_COLOR, border=1,
                    relief="solid", highlightbackground=BORDER,
                    padx=14, pady=8, cursor="hand2",
                    command=lambda: shift_line_to_left(e.get(1.0, END)))
leftShift.pack(fill="x", pady=(0, 10))
leftShift.bind("<Enter>", pointerInside)
leftShift.bind("<Leave>", pointerOutside)

start_typing = Button(btn_frame, text="Start AutoTyping", activebackground=ACCENT_HOVER,
                       activeforeground="#ffffff",
                       font=("Segoe UI", 13, "bold"), border=0,
                       bg=ACCENT, fg="#ffffff", cursor="hand2",
                       pady=10,
                       command=lambda: typei(s.get(), x.get()))
start_typing.pack(fill="x", pady=(0, 10))
start_typing.bind("<Enter>", lambda ev: ev.widget.config(bg=ACCENT_HOVER) if str(ev.widget['state']) != 'disabled' else None)
start_typing.bind("<Leave>", lambda ev: ev.widget.config(bg=ACCENT) if str(ev.widget['state']) != 'disabled' else None)

cancel_btn = Button(btn_frame, text="Cancel (Esc)", activebackground="#f4c9c9",
                     activeforeground="#7a1f1f",
                     font=("Segoe UI", 11), border=1, relief="solid",
                     highlightbackground=BORDER,
                     bg=CARD, fg="#b03a3a", cursor="arrow",
                     padx=14, pady=8, state="disabled",
                     command=stop_typing)
cancel_btn.pack(fill="x")
cancel_btn.bind("<Enter>", lambda ev: ev.widget.config(bg="#f4dede") if str(ev.widget['state']) != 'disabled' else None)
cancel_btn.bind("<Leave>", lambda ev: ev.widget.config(bg=CARD) if str(ev.widget['state']) != 'disabled' else None)

root.bind("<Escape>", stop_typing)

root.mainloop()