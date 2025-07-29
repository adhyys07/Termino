import random
import time
import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def draw_plinko_board(path=None, slot_count=7, rows=6):
    board_width = slot_count * 3
    pad = (os.get_terminal_size().columns - board_width) // 2 if hasattr(os, 'get_terminal_size') else 0
    def center_line(line):
        return " " * pad + line

    extra_col = 2
    if path:
        for row in range(len(path)):
            line = ""
            for col in range(slot_count):
                if path[row] == col:
                    line += " o "
                else:
                    line += " . "
            line += " . " * extra_col
            print(center_line(line))
    else:
        for row in range(rows + 1):
            print(center_line((" . " * slot_count) + (" . " * extra_col)))
    print(center_line("=" * (board_width + extra_col * 3)))
    multipliers = [0.5, 1, 2, 5, 2, 1, 0.5]
    print(center_line(" ".join(f"{m:^3}" for m in multipliers) + "   " * extra_col))

def play_plinko(user):
    from airtable0.users import update_coins
    print("\n--- Plinko ---\n")
    print("Drop a ball and win coins based on where it lands!")
    print("Board: 7 slots (0-6). Multipliers: [0.5, 1, 2, 5, 2, 1, 0.5]")

    multipliers = [0.5, 1, 2, 5, 2, 1, 0.5]
    slot_count = len(multipliers)
    rows = 6

    print(f"You have {user['coins']} coins.")
    while True:
        try:
            bet = int(input("Enter your bet (or 0 to exit): "))
            if bet == 0:
                print("Exiting Plinko...")
                break
            if bet < 0 or bet > user['coins']:
                print("Invalid bet amount.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        slot = slot_count // 2
        path = [slot]
        print("\nDropping ball...\n")
        time.sleep(1)

        for _ in range(rows):
            move = random.choice([-1, 1])
            slot += move
            slot = max(0, min(slot_count - 1, slot))
            path.append(slot)
            clear()
            draw_plinko_board(path, slot_count, rows)
            time.sleep(0.3)

        final_slot = path[-1]
        multiplier = multipliers[final_slot]
        win = int(bet * multiplier)

        print(f"\n🎯 Ball landed in slot {final_slot}!")
        print(f"🏆 Multiplier: {multiplier}x")
        print(f"You {'won' if win > 0 else 'lost'} {win} coins.")
        user['coins'] += win - bet
        user_id = user.get('id')
        if user_id:
            update_coins(user_id, user['coins'])
        print(f"💰 Your new balance: {user['coins']:.2f} coins.")


        again = input("\nPress Enter to play again or type 'q' to quit: ")
        if again.lower() == 'q':
            break
    return user
