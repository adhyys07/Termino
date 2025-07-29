
import random
import time
import os
import sys

symbols = ['🍒', '🍋', '🔔', '💎', '7️⃣', '🍀']
payouts = {
    '🍒': 2,
    '🍋': 3,
    '🔔': 5,
    '💎': 10,
    '7️⃣': 20,
    '🍀': 50
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slot_grid(grid, highlight_row=None):
    print("\n+-------+-------+-------+")
    for i, row in enumerate(grid):
        row_str = "|"
        for sym in row:
            row_str += f"  {sym}   |"
        if highlight_row is not None and i == highlight_row:
            print(f">{row_str} <")
        else:
            print(f" {row_str} ")
        print("+-------+-------+-------+")

def spin_animation_grid(spins=12, delay=0.08):
    grid = [[random.choice(symbols) for _ in range(3)] for _ in range(3)]
    for spin in range(spins):
        for r in range(3):
            grid[r] = [random.choice(symbols) for _ in range(3)]
            clear()
            print("🎰 Terminal Slots 🎰")
            print_slot_grid(grid, highlight_row=r)
            time.sleep(delay)
    clear()
    print("🎰 Terminal Slots 🎰")
    print_slot_grid(grid)
    return grid

def evaluate_grid(grid):
    row = grid[1]
    if row[0] == row[1] == row[2]:
        symbol = row[0]
        multiplier = payouts[symbol]
        return True, multiplier, symbol
    if row[0] == row[1]:
        symbol = row[0]
        return True, 1, symbol  
    if row[1] == row[2]:
        symbol = row[1]
        return True, 1, symbol
    if grid[0][0] == grid[1][1] == grid[2][2]:
        symbol = grid[1][1]
        return True, 4, symbol 
    if grid[0][2] == grid[1][1] == grid[2][0]:
        symbol = grid[1][1]
        return True, 4, symbol
    if '7️⃣' in row:
        return True, 2, '7️⃣'
    return False, 0, None

def play_slots(session):
    from airtable0.users import get_user_balance, update_coins
    username = session.get('username')
    user_id = session.get('id')
    if not username or not user_id:
        print("❌ User session invalid. Please login again.")
        return session, False

    while True:
        balance = get_user_balance(username)
        if balance is None:
            print("❌ Could not retrieve balance from database.")
            return session, False

        bet = input(f"\nBalance: {balance} | Enter bet amount (or Q to quit): ")
        if bet.lower() == 'q':
            print("👋 Thanks for playing!")
            return session, False

        if not bet.isdigit():
            print("❌ Invalid bet.")
            continue

        bet = int(bet)
        if bet <= 0 or bet > balance:
            print("❌ Invalid or insufficient balance.")
            continue

        print("\nSpinning...")
        grid = spin_animation_grid()

        win, multiplier, symbol = evaluate_grid(grid)
        if win:
            capped_multiplier = min(multiplier, 40)
            winnings = bet * capped_multiplier
            if capped_multiplier != multiplier:
                print(f"\n🎉 MAX WIN CAP! You win {winnings} (x40)!")
            elif multiplier == payouts.get(symbol, 0):
                print(f"\n🎉 JACKPOT! {symbol*3} You won {winnings} (x{multiplier})!")
            elif multiplier == 1:
                print(f"\n✨ Two of a kind! {symbol}{symbol} You win your bet back!")
            elif multiplier == 4:
                print(f"\n💎 Diagonal match! {symbol}{symbol}{symbol} You win {winnings} (x4)!")
            elif multiplier == 2 and symbol == '7️⃣':
                print(f"\n7️⃣ Lucky 7! You win {winnings} (x2)!")
            else:
                print(f"\n🎉 You win {winnings} (x{multiplier})!")
            balance += winnings
        else:
            print("\n😢 No luck this time. Only the middle row and special combos pay!")
            balance -= bet

        update_coins(user_id, balance)
        session['coins'] = balance

        again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if again != 'y':
            print("👋 Thanks for playing!")
            return session, False

