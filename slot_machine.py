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

# Load images
bg_image = Image.open("background.jpeg")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Load symbols and button images
reel_images = {
    "A": ImageTk.PhotoImage(Image.open("symbol_A.png")),
    "B": ImageTk.PhotoImage(Image.open("symbol_B.png")),
    "C": ImageTk.PhotoImage(Image.open("symbol_C.png")),
    "D": ImageTk.PhotoImage(Image.open("symbol_D.png"))
}

spin_button_image = ImageTk.PhotoImage(Image.open("spin_button.jpeg"))
deposit_button_image = ImageTk.PhotoImage(Image.open("deposit_button.jpeg"))

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

# Create labels for the slot reels
reel_labels = []
for i in range(COLS):
    reel_label = tk.Label(root, bg="white", width=10, height=5, borderwidth=2, relief="solid")
    reel_label.place(x=200 + i*100, y=200)
    reel_labels.append(reel_label)

def spin_animation(spins=20):
    for _ in range(spins):
        for reel_label in reel_labels:
            reel_label.config(image=random.choice(list(reel_images.values())))
        root.update_idletasks()
        time.sleep(0.1)

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

# UI Elements
balance_label = tk.Label(root, text=f"Balance: ${balance}", font=("Helvetica", 16), bg="lightblue", fg="black", padx=10, pady=5)
balance_label.place(x=50, y=50)

deposit_entry = tk.Entry(root)
deposit_entry.place(x=50, y=100)
deposit_button = tk.Button(root, image=deposit_button_image, command=deposit)
deposit_button.place(x=200, y=90)

lines_entry = tk.Entry(root)
lines_entry.place(x=50, y=150)
lines_entry.insert(0, "1")

bet_entry = tk.Entry(root)
bet_entry.place(x=50, y=200)
bet_entry.insert(0, "1")

spin_button = tk.Button(root, image=spin_button_image, command=spin)
spin_button.place(x=200, y=250)

slot_text = tk.StringVar()
slot_label = tk.Label(root, textvariable=slot_text, font=("Helvetica", 16), bg="white", fg="black", width=30, height=10, borderwidth=2, relief="solid")
slot_label.place(x=200, y=300)

winnings_text = tk.StringVar()
winnings_label = tk.Label(root, textvariable=winnings_text, font=("Helvetica", 16), bg="white", fg="black", width=30, height=3, borderwidth=2, relief="solid")
winnings_label.place(x=200, y=420)

# Start the main loop
root.mainloop()
