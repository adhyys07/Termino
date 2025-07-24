import random
from core.economy import can_bet, apply_bet
from airtable0 import users

def play_wheel_of_fortune(user):
    import time, sys

    while True:
        print("\n--- Wheel of Fortune ---")
        try:
            bet = int(input("Enter your bet: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if not can_bet(user, bet):
            print("Not enough coins or invalid bet amount.")
            continue

        wheel = [
            (0, "Bankrupt"),
            (0.5, "Half Bet"),
            (1, "Break Even"),
            (2, "Double"),
            (5, "Jackpot!"),
            (7.5, "Mega Win"),
            (10, "Ultra Win!")
        ]

        # Wheel animation
        print()
        for _ in range(10):
            for seg in wheel:
                sys.stdout.write(f"Spinning... {seg[1]}   \r")
                sys.stdout.flush()
                time.sleep(0.08)

        print(" " * 30)
        segment = random.choice(wheel)
        print(f"The wheel lands on: {segment[1]}")

        # Always subtract the bet first
        user['Coins'] = user.get('Coins', user.get('coins', 0))  # Ensure Coins field exists
        user['Coins'] -= bet
        if segment[0] == 0:
            print("You lost your bet!")
        elif segment[0] == 0.5:
            print("You get half your bet back.")
            user['Coins'] += int(bet * 0.5)
        elif segment[0] == 1:
            print("You break even.")
            user['Coins'] += bet
        elif segment[0] == 2:
            print("You win double your bet!")
            user['Coins'] += int(bet * 2)
        elif segment[0] == 5:
            print("Jackpot! You win 5x your bet!")
            user['Coins'] += int(bet * 5)
        elif segment[0] == 7.5:
            print("Mega Win! You win 7.5x your bet!")
            user['Coins'] += int(bet * 7.5)
        elif segment[0] == 10:
            print("Ultra Win! You win 10x your bet!")
            user['Coins'] += int(bet * 10)
        print(f"Total balance: {user['Coins']}")

        # Ask to play again
        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Returning to the games dashboard...")
            break
