def play_blackjack(user):
    from airtable0.users import update_coins, log_play
    import random
    print("--- Blackjack ---\n")

    def card_ascii(card):
        faces = {11: 'A', 10: '10', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}
        suits = ['♠', '♥', '♦', '♣']
        suit = random.choice(suits)
        face = faces.get(card, str(card))
        return f"┌─────┐\n|{face:<2}   |\n|  {suit}  |\n|   {face:>2}|\n└─────┘"

    def print_hand(hand, hide_second=False):
        lines = [card_ascii(card).split('\n') for card in hand]
        if hide_second and len(lines) > 1:
            lines[1] = ["┌─────┐", "|░░░░|", "|░░░░|", "|░░░░|", "└─────┘"]
        for i in range(5):
            print('  '.join(card[i] for card in lines))

    coins = user.get('Coins', user.get('coins', 0))
    user_id = user.get('id')
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
            print("Exiting Blackjack...")
            return user
        if bet < 0 or bet > coins:
            print("Invalid bet amount.")
            continue
        break

    initial_balance = coins

    def deal_card():
        cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        return random.choice(cards)

    def hand_value(hand):
        value = sum(hand)
        aces = hand.count(11)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    player = [deal_card(), deal_card()]
    dealer = [deal_card(), deal_card()]

    print("Your hand:")
    print_hand(player)
    print(f"Total: {hand_value(player)}")
    print("Dealer shows:")
    print_hand([dealer[0], dealer[1]], hide_second=True)

    # Player turn
    bust = False
    while True:
        if hand_value(player) == 21:
            print("Blackjack! Let's see the dealer...")
            break
        move = input("Hit or Stand? (h/s): ").strip().lower()
        if move == 'h':
            player.append(deal_card())
            print("Your hand:")
            print_hand(player)
            print(f"Total: {hand_value(player)}")
            if hand_value(player) > 21:
                print("Bust! You lose your bet.")
                coins -= bet
                user['Coins'] = coins
                update_coins(user_id, coins)
                bust = True
                break
        elif move == 's':
            break
        else:
            print("Invalid input. Type 'h' to hit or 's' to stand.")

    if not bust:
        print("Dealer's hand:")
        print_hand(dealer)
        print(f"Total: {hand_value(dealer)}")
        while hand_value(dealer) < 17:
            dealer.append(deal_card())
            print("Dealer hits:")
            print_hand(dealer)
            print(f"Total: {hand_value(dealer)}")
        dealer_total = hand_value(dealer)
        player_total = hand_value(player)

        if dealer_total > 21:
            print("Dealer busts! You win 2x your bet!")
            coins += bet
            result_str = "Dealer busts"
        elif player_total > dealer_total:
            print("You win! You win 2x your bet!")
            coins += bet
            result_str = "Player wins"
        elif player_total == dealer_total:
            print("Push! Your bet is returned.")
            result_str = "Push"
        else:
            print("Dealer wins. You lose your bet.")
            coins -= bet
            result_str = "Dealer wins"

        user['Coins'] = coins
        update_coins(user_id, coins)
    else:
        result_str = "Player busts"

    print(f"Your new balance: {coins} coins.")

    # Log play
    if user_id:
        profit = coins - initial_balance
        log_play(
            user_id=user_id,
            username=user.get('username', ''),
            game="Blackjack",
            bet=bet,
            profit=profit,
            result=result_str,
            balance_after=coins,
            extra=None
        )
    return user
