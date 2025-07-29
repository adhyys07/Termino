import random
import time
import os
import json
import base64

def clear():
    os.system("cls" if os.name == "nt" else "clear")

ROULETTE_NUMBERS = list(range(37))
RED_NUMBERS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
BLACK_NUMBERS = set(ROULETTE_NUMBERS) - RED_NUMBERS - {0}

def spin_animation(final_number):
    wheel = ROULETTE_NUMBERS * 2
    start = random.randint(0, len(wheel) - 20)
    for i in range(20):
        clear()
        print("🎡 Spinning Roulette...\n")
        for j in range(10):
            pointer = " ⮕ " if j == 9 else "   "
            number = wheel[start + i + j]
            color = get_color(number)
            print(f"{pointer}[{color}] {number}")
        time.sleep(0.1 + i * 0.01)
    return wheel[start + 19 + 9]

def get_color(number):
    if number == 0:
        return "Green"
    elif number in RED_NUMBERS:
        return "Red"
    else:
        return "Black"

def play_roulette(user):
    def print_roulette_table():
        print("\n   ┌───────────────────────────────────────────────┐")
        print("   │  0  │  1  2  3 │  4  5  6 │  7  8  9 │ 10 11 12 │")
        print("   │ 13 14 15 │ 16 17 18 │ 19 20 21 │ 22 23 24 │ 25 26 27 │")
        print("   │ 28 29 30 │ 31 32 33 │ 34 35 36 │")
        print("   └───────────────────────────────────────────────┘")
        print("   🟥 Red:  1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36")
        print("   ⬛ Black: All others except 0 (Green)")

    print("\n🎰 Welcome to Terminal Roulette!")
    print(f"💰 You have {user['coins']} coins.")

    while True:
        print_roulette_table()
        print("\n--- Place Your Bet ---")
        print("Options:")
        print("  1. Bet on color (red/black/green)")
        print("")
        print("  2. Bet on a specific number (0-36)")
        print("")
        print("  3. Bet on a range of numbers (e.g. 1-12)")
        print("")
        print("Payouts: color → 8x, number → 20x, range → (32/range_size)x")
        print("")
        bet_type = input("Choose bet type (color/number/range): ").strip().lower()
        

        if bet_type == "color" or bet_type == "1":
            choice = input("Bet on color (red/black/green): ").strip().lower()
            if choice not in ["red", "black", "green"]:
                print("❌ Invalid color. Try again.")
                continue
        elif bet_type == "number" or bet_type == "2":
            try:
                choice = int(input("Bet on number (0-36): "))
                if choice < 0 or choice > 36:
                    print("❌ Invalid number.")
                    continue
            except:
                print("❌ Please enter a valid number.")
                continue
        elif bet_type == "range" or bet_type == "3":
            try:
                range_str = input("Enter range (e.g. 1-12): ").replace(" ","")
                start, end = map(int, range_str.split("-"))
                if start < 0 or end > 36 or start >= end:
                    print("❌ Invalid range.")
                    continue
            except:
                print("❌ Please enter a valid range.")
                continue
        else:
            print("❌ Invalid bet type.")
            continue

        try:
            bet = int(input("Enter your bet amount (0 to exit): "))
            if bet == 0:
                print("Exiting roulette...")
                break
            if bet < 0 or bet > user['coins']:
                print("❌ Invalid bet amount.")
                continue
        except:
            print("❌ Please enter a valid number.")
            continue

        print("\n🌀 Spinning...")
        user['coins'] -= bet
        winning_number = spin_animation(bet)
        winning_color = get_color(winning_number)

        print(f"\n🎯 Ball landed on {winning_number} ({winning_color})")

        win = 0
        if bet_type == "color":
            if (choice == "red" and winning_color == "Red") or \
               (choice == "black" and winning_color == "Black") or \
               (choice == "green" and winning_color == "Green"):
                win = bet * 8
        elif bet_type == "number":
            if winning_number == choice:
                win = bet * 20
        elif bet_type == "range":
            if winning_number >= start and winning_number <= end:
                range_size = end - start + 1
                win = int(bet * (36 / range_size))

        if win > 0:
            print(f"🏆 You won {win} coins!")
        else:
            print("💥 You lost the bet.")

        user['coins'] += win
        print(f"💰 Your balance: {user['coins']} coins")

        again = input("\nPress Enter to play again or type 'q' to quit: ")
        if again.lower() == 'q':
            break
    return user
