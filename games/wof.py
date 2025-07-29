import random
from core.economy import can_bet, apply_bet
from airtable0 import users

def play_wheel_of_fortune(user):
    import time, sys

    from airtable0.users import log_play
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
            (0, "Bankrupt"), (0, "Bankrupt"), (0, "Bankrupt"), (0, "Bankrupt"),
            (0, "Bankrupt"),  # 5 out of 25 = 20%
            (0.5, "Half Bet"), (0.5, "Half Bet"),
            (1, "Break Even"), (1, "Break Even"),
            (2, "Double"), (2, "Double"),
            (5, "Jackpot!"),
            (7.5, "Mega Win"),
            (10, "Ultra Win!"),
            (0.5, "Half Bet"), (1, "Break Even"), (2, "Double"),
            (5, "Jackpot!"), (7.5, "Mega Win"), (10, "Ultra Win!"),
            (2, "Double"), (1, "Break Even"), (0.5, "Half Bet"), (5, "Jackpot!")
        ]

        print()
        for _ in range(10):
            for seg in wheel:
                sys.stdout.write(f"Spinning... {seg[1]}   \r")
                sys.stdout.flush()
                time.sleep(0.08)

        print(" " * 30)
        segment = random.choice(wheel)
        print(f"The wheel lands on: {segment[1]}")

        user['Coins'] = user.get('Coins', user.get('coins', 0))
        user_id = user.get('id')
        username = user.get('username', '')
        initial_balance = user['Coins']
        user['Coins'] -= bet
        profit = 0  
        result = segment[1]
        if segment[0] == 0:
            print("You lost your bet!")
            if user_id is not None:
                users.update_coins(user_id, user['Coins'])
            profit = -bet
            print(f"Total balance: {user['Coins']}")
        elif segment[0] == 0.5:
            print("You get half your bet back.")
            half_back = int(bet * 0.5)
            user['Coins'] += half_back
            if user_id is not None:
                users.update_coins(user_id, user['Coins'])
            profit = -bet + half_back
            print(f"You got back {half_back} coins. Total balance: {user['Coins']}")
        elif segment[0] == 1:
            print("You break even.")
            user['Coins'] += bet
            if user_id is not None:
                users.update_coins(user_id, user['Coins'])
            profit = 0
            print(f"Total balance: {user['Coins']}")
        else:
            winnings = int(bet * segment[0])
            print(f"You win {segment[0]}x your bet! You won {winnings} coins!")
            user['Coins'] += winnings
            if user_id is not None:
                users.update_coins(user_id, user['Coins'])
            profit = winnings
            print(f"Total balance: {user['Coins']}")

        # Log play
        if user_id is not None:
            log_play(
                user_id=user_id,
                username=username,
                game="Wheel of Fortune",
                bet=bet,
                profit=profit,
                result=result,
                balance_after=user['Coins'],
                extra=None
            )

        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Returning to the games dashboard...")
            break
    return user
