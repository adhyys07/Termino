import random

def print_dice(dice):
    dice_art = {
        1: [
            "┌─────┐",
            "|     |",
            "|  ●  |",
            "|     |",
            "└─────┘"
        ],
        2: [
            "┌─────┐",
            "| ●   |",
            "|     |",
            "|   ● |",
            "└─────┘"
        ],
        3: [
            "┌─────┐",
            "| ●   |",
            "|  ●  |",
            "|   ● |",
            "└─────┘"
        ],
        4: [
            "┌─────┐",
            "| ● ● |",
            "|     |",
            "| ● ● |",
            "└─────┘"
        ],
        5: [
            "┌─────┐",
            "| ● ● |",
            "|  ●  |",
            "| ● ● |",
            "└─────┘"
        ],
        6: [
            "┌─────┐",
            "| ● ● |",
            "| ● ● |",
            "| ● ● |",
            "└─────┘"
        ]
    }
    lines = [dice_art[d] for d in dice]
    for i in range(5):
        print('  '.join(line[i] for line in lines))

def play_craps(user):
    from airtable0.users import update_coins
    from airtable0.users import log_play
    while True:
        print("\n--- Craps ---\n")
        coins = user.get('Coins', user.get('coins', 0))
        user_id = user.get('id')
        username = user.get('username', '')
        if coins <= 0:
            print("You have no coins to bet!")
            return user
        if not user_id:
            print("User ID not found. Cannot update coins in database.")
            return user

        while True:
            try:
                bet = int(input(f"You have {coins} coins. Enter your bet (0 to exit): "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if bet == 0:
                print("Exiting Craps...")
                return user
            if bet < 0 or bet > coins:
                print("Invalid bet amount.")
                continue
            break

        initial_balance = coins

        def roll_dice():
            return random.randint(1, 6), random.randint(1, 6)

        dice = roll_dice()
        total = sum(dice)
        print("You roll:")
        print_dice(dice)
        print(f"Total: {total}")

        result_str = ""
        if total in [7, 11]:
            print("Natural! You win 2x your bet!")
            coins += bet
            result_str = "Natural win"
            user['Coins'] = coins
            update_coins(user_id, coins)
            print(f"Your new balance: {coins} coins.")
        elif total in [2, 3, 12]:
            print("Craps! You lose your bet.")
            coins -= bet
            result_str = "Craps loss"
            user['Coins'] = coins
            update_coins(user_id, coins)
            print(f"Your new balance: {coins} coins.")
        else:
            point = total
            print(f"Point is set to {point}. Keep rolling!")

            # Point phase
            while True:
                input("Press Enter to roll the dice...")
                dice = roll_dice()
                total = sum(dice)
                print("You roll:")
                print_dice(dice)
                print(f"Total: {total}")
                if total == point:
                    print("You hit your point! You win 2x your bet!")
                    coins += bet
                    result_str = f"Hit point {point}"
                    break
                elif total == 7:
                    print("Seven out! You lose your bet.")
                    coins -= bet
                    result_str = "Seven out"
                    break
                else:
                    print("Roll again!")
            user['Coins'] = coins
            update_coins(user_id, coins)
            print(f"Your new balance: {coins} coins.")

        # Log play
        if user_id:
            profit = coins - initial_balance
            log_play(
                user_id=user_id,
                username=username,
                game="Craps",
                bet=bet,
                profit=profit,
                result=result_str,
                balance_after=coins,
                extra=None
            )

        again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if again != 'y':
            print("👋 Thanks for playing!")
            return user
