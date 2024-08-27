import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import time
import pygame

# Initialize Pygame for sound
pygame.mixer.init()

# Initialize the main window
root = tk.Tk()
root.title("Slot Machine Game")
root.geometry("800x600")
root.configure(bg="lightblue")

# Load images
bg_image = Image.open("background.jpeg").resize((800, 600), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Load symbols and button images
reel_images = {
    "A": ImageTk.PhotoImage(Image.open("symbol_A.png").resize((80, 80), Image.LANCZOS)),
    "B": ImageTk.PhotoImage(Image.open("symbol_B.png").resize((80, 80), Image.LANCZOS)),
    "C": ImageTk.PhotoImage(Image.open("symbol_C.png").resize((80, 80), Image.LANCZOS)),
    "D": ImageTk.PhotoImage(Image.open("symbol_D.png").resize((80, 80), Image.LANCZOS))
}

spin_button_image = ImageTk.PhotoImage(Image.open("spin_button.jpeg").resize((100, 50), Image.LANCZOS))
deposit_button_image = ImageTk.PhotoImage(Image.open("deposit_button.jpeg").resize((100, 50), Image.LANCZOS))

# Load sound effects
spin_sound = pygame.mixer.Sound("spin.wav")
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")

# Global variables
balance = 0
ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

# Functions

def deposit():
    global balance
    amount = deposit_entry.get()
    if amount.isdigit():
        balance += int(amount)
        balance_label.config(text=f"Balance: ${balance}")
        deposit_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Invalid Input", "Please enter a valid number")

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        all_symbols.extend([symbol] * symbol_count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)

    return columns

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if column[line] != symbol:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def spin_animation(spins=20):
    for _ in range(spins):
        for reel_label in reel_labels:
            reel_label.config(image=random.choice(list(reel_images.values())))
        root.update_idletasks()
        time.sleep(0.1)

def spin():
    global balance
    lines = int(lines_entry.get())
    bet = int(bet_entry.get())
    total_bet = lines * bet
    
    if total_bet > balance:
        messagebox.showerror("Insufficient Funds", "You do not have enough balance for this bet")
        return
    
    balance -= total_bet
    balance_label.config(text=f"Balance: ${balance}")
    
    pygame.mixer.Sound.play(spin_sound)
    spin_animation()
    
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    for i, reel_label in enumerate(reel_labels):
        reel_label.config(image=reel_images[slots[i][0]])
    
    winnings, winnings_lines = check_winnings(slots, lines, bet, symbol_value)
    balance += winnings
    balance_label.config(text=f"Balance: ${balance}")
    
    if winnings > 0:
        pygame.mixer.Sound.play(win_sound)
    else:
        pygame.mixer.Sound.play(lose_sound)
    
    slot_text.set("\n".join([" | ".join(row) for row in zip(*slots)]))
    winnings_text.set(f"You Won ${winnings} on lines {', '.join(map(str, winnings_lines)) if winnings_lines else 'none'}")

# Create frames for layout
top_frame = tk.Frame(root, bg="lightblue", height=100)
top_frame.pack(fill=tk.X, pady=10)
top_frame.pack_propagate(False)

mid_frame = tk.Frame(root, bg="lightblue", height=200)
mid_frame.pack(fill=tk.X, pady=20)
mid_frame.pack_propagate(False)

bottom_frame = tk.Frame(root, bg="lightblue", height=100)
bottom_frame.pack(fill=tk.X, pady=10)
bottom_frame.pack_propagate(False)

# Balance label
balance_label = tk.Label(top_frame, text=f"Balance: ${balance}", font=("Helvetica", 16), bg="lightblue", fg="black")
balance_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Deposit entry and button
deposit_entry = tk.Entry(top_frame, width=15)
deposit_entry.grid(row=0, column=1, padx=10)
deposit_button = tk.Button(top_frame, image=deposit_button_image, command=deposit)
deposit_button.grid(row=0, column=2, padx=10)

# Create labels for the slot reels
reel_labels = []
for i in range(COLS):
    reel_label = tk.Label(mid_frame, bg="white", width=80, height=80, borderwidth=2, relief="solid")
    reel_label.grid(row=0, column=i, padx=10, pady=10)
    reel_labels.append(reel_label)

# Lines and Bet entry
lines_label = tk.Label(bottom_frame, text="Lines:", font=("Helvetica", 14), bg="lightblue", fg="black")
lines_label.grid(row=0, column=0, padx=5)
lines_entry = tk.Entry(bottom_frame, width=5)
lines_entry.grid(row=0, column=1, padx=5)
lines_entry.insert(0, "1")

bet_label = tk.Label(bottom_frame, text="Bet:", font=("Helvetica", 14), bg="lightblue", fg="black")
bet_label.grid(row=0, column=2, padx=5)
bet_entry = tk.Entry(bottom_frame, width=5)
bet_entry.grid(row=0, column=3, padx=5)
bet_entry.insert(0, "1")

# Spin button
spin_button = tk.Button(bottom_frame, image=spin_button_image, command=spin)
spin_button.grid(row=0, column=4, padx=10)

# Winnings and slot text
slot_text = tk.StringVar()
slot_label = tk.Label(root, textvariable=slot_text, font=("Helvetica", 16), bg="white", fg="black", width=40, height=10, borderwidth=2, relief="solid")
slot_label.pack(pady=10)

winnings_text = tk.StringVar()
winnings_label = tk.Label(root, textvariable=winnings_text, font=("Helvetica", 16), bg="white", fg="black", width=40, height=3, borderwidth=2, relief="solid")
winnings_label.pack(pady=10)

# Start the main loop
root.mainloop()
