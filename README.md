# 🎰 Slot Machine Game

A simple GUI-based slot machine game written in Python using Tkinter and Pygame. This game allows you to deposit money, place bets on multiple lines, and spin the slot machine to test your luck. The game calculates your winnings and updates your balance after each spin.

## Features

- **Deposit System**: Start by depositing an amount of your choice.
- **Multi-line Betting**: Bet on 1 to 3 lines with customizable bet amounts.
- **Slot Machine Simulation**: Randomized slot machine spins with four unique symbols (A, B, C, D).
- **Winning Calculation**: The game checks if you've won on any lines and adjusts your balance accordingly.
- **Spin Animation**: Visual spin animation for the slot reels.

## Symbols and Payouts

| Symbol | Count | Payout |
|--------|-------|--------|
| A      | 2     | 5x     |
| B      | 4     | 4x     |
| C      | 6     | 3x     |
| D      | 8     | 2x     |

- **A** is the rarest symbol and pays the highest.
- **D** is the most common symbol and pays the lowest.

## How to Play

1. **Deposit**: Start by entering the amount you would like to deposit.
2. **Choose Lines**: Select the number of lines to bet on (1-3 lines).
3. **Place Your Bet**: Enter the amount you want to bet on each line.
4. **Spin the Slots**: Press the "Spin" button to spin the slot machine.
5. **Check Your Winnings**: The game will display the amount you've won and update your balance.
6. **Continue or Quit**: You can keep playing until you decide to quit by pressing the "Deposit" button.

## Running the Game

To run the game, ensure you have Python installed along with the required libraries. Then, simply execute the script in your terminal:

```bash
python slot_machine.py

```

## Example

1. **Deposit**: $100
2. **Number of Lines**: 2
3. **Bet per Line**: $10
4. **Total Bet**: $20
5. **Remaining Balance**: $80

    ```
    A | C | B
    A | C | D
    ```

6. **Winnings**: You Won $50 on lines: 1

## Dependencies

- Python 3.x
- Tkinter
- Pygame
- Pillow (PIL Fork)

You can install the necessary Python packages using pip:

```bash
pip install pygame pillow