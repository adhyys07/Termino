import random
from core.economy import can_bet, apply_bet

def play_wheel_of_fortune(user):
    print("\n--- Wheel of Fortune ---")
    try:
        bet = int(input("Enter your bet: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return user
    if not can_bet(user, bet):
        print("Not enough coins or invalid bet amount.")
        return user
    # Define wheel segments and multipliers
    wheel = [
        (0, "Bankrupt"),
        (0.5, "Half Bet"),
        (1, "Break Even"),
        (2, "Double"),
        (5, "Jackpot!")
    ]
    segment = random.choice(wheel)
    print(f"The wheel lands on: {segment[1]}")
    if segment[0] == 0:
        print("You lost your bet!")
        user = apply_bet(user, bet, 0)
    elif segment[0] == 0.5:
        print("You get half your bet back.")
        user = apply_bet(user, int(bet/2), 0)
    elif segment[0] == 1:
        print("You break even.")
        # No change to coins
    else:
        winnings = int(bet * segment[0])
        print(f"You win {winnings} coins!")
        user = apply_bet(user, bet, segment[0])
    print(f"Your new balance: {user['coins']} coins.")
    return user
