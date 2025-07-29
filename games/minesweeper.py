
import random
import os
import time

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def draw_board(board, revealed, mines):
    print("   " + " ".join([f"{i:^7}" for i in range(len(board[0]))]))
    for r, row in enumerate(board):
        line = f"{r:2} "
        for c, cell in enumerate(row):
            if (r, c) in revealed:
                if (r, c) in mines:
                    line += "   *    "  # Mine
                else:
                    line += "   o    "  # Safe cell
            else:
                line += "   #    "  # Hidden
        print(line)

def get_neighbors(r, c, rows, cols):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                yield nr, nc

def play_minesweeper(user):
    from airtable0.users import update_coins
    print("\n--- Terminal Minesweeper ---\n")
    rows, cols = 8, 8
    print(f"Board size: {rows}x{cols}")
    print(f"You have {user['coins']} coins.")
    while True:
        try:
            num_mines = int(input(f"How many mines? (1-{rows*cols-1}): "))
            if num_mines < 1 or num_mines >= rows*cols:
                print("Invalid number of mines.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        try:
            bet = int(input("Enter your bet (or 0 to exit): "))
            if bet == 0:
                print("Exiting Minesweeper...")
                return user
            if bet < 0 or bet > user['coins']:
                print("Invalid bet amount.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        # Per-vault profit: higher for more mines, lower for fewer mines
        max_multiplier = 32
        base_multiplier = 2 + num_mines // 2
        multiplier = min(max_multiplier, base_multiplier)
        per_vault_profit = bet * (multiplier / ((rows * cols) - num_mines))
        print(f"Multiplier for clearing all: {multiplier}x")
        print(f"Profit per safe vault: {per_vault_profit:.2f} coins (Multiplier: {multiplier}x)")

        # Setup board and variables for this round
        board = [[0 for _ in range(cols)] for _ in range(rows)]
        mines = set()
        while len(mines) < num_mines:
            r, c = random.randint(0, rows-1), random.randint(0, cols-1)
            mines.add((r, c))
        for r, c in mines:
            for nr, nc in get_neighbors(r, c, rows, cols):
                board[nr][nc] += 1

        revealed = set()  # re-initialize for each round
        user['coins'] -= bet
        user_id = user.get('id')
        if user_id:
            update_coins(user_id, user['coins'])
        profit = 0.0
        clear()
        draw_board(board, revealed, mines)

        while True:
            print(f"Coins: {user['coins']} | Bet: {bet} | Profit: {profit:.2f}")
            print("Type 'q' to quit and take your profit, or reveal a cell (e.g. r 3 4): ")
            action = input().strip().lower()
            if action == 'q':
                user['coins'] += bet + profit
                if user_id:
                    update_coins(user_id, user['coins'])
                print(f"You quit and took your profit! {bet + profit:.2f} coins added. Balance: {user['coins']:.2f}")
                break
            parts = action.split()
            if len(parts) != 3 or parts[0] != 'r':
                print("Invalid input. Use r row col or 'q' to quit.")
                continue
            try:
                r, c = int(parts[1]), int(parts[2])
                if not (0 <= r < rows and 0 <= c < cols):
                    print("Out of bounds.")
                    continue
            except ValueError:
                print("Invalid row/col.")
                continue

            if (r, c) in revealed:
                
                clear()
                draw_board(board, revealed, mines)
                print("Already revealed.")
                continue
            if (r, c) in mines:
                revealed.add((r, c))
                clear()
                draw_board(board, revealed, mines)
                print(f"\U0001F4A5 You hit a mine! You lost your bet and all profit. Balance: {user['coins']:.2f}")
                if user_id:
                    update_coins(user_id, user['coins'])
                break
            elif board[r][c] == 0:
                stack = [(r, c)]
                newly_revealed = set()
                while stack:
                    cr, cc = stack.pop()
                    if (cr, cc) in revealed or (cr, cc) in mines:
                        continue
                    revealed.add((cr, cc))
                    newly_revealed.add((cr, cc))
                    if board[cr][cc] == 0:
                        for nr, nc in get_neighbors(cr, cc, rows, cols):
                            if (nr, nc) not in revealed and (nr, nc) not in mines:
                                stack.append((nr, nc))
                profit += per_vault_profit * len(newly_revealed)
                clear()
                draw_board(board, revealed, mines)
            else:
                revealed.add((r, c))
                profit += per_vault_profit
                clear()
                draw_board(board, revealed, mines)
            balance_if_quit = user['coins'] + bet + profit
            print(f"Profit so far: {profit:.2f} coins. Balance if you quit now: {balance_if_quit:.2f}")
            if len(revealed) == rows * cols - num_mines:
                win = bet * multiplier
                total_win = bet + win  
                print(f"\U0001F3C6 You cleared the board! You win {win} coins (plus your bet back, total: {total_win} coins).")
                user['coins'] += total_win - profit
                if user_id:
                    update_coins(user_id, user['coins'])
                break
        again = input("\nPress Enter to play again or type 'q' to quit: ")
        if again.lower() == 'q':
            break
    return user