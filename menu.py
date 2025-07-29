from games.wof import play_wheel_of_fortune
from games.plinko import play_plinko
from games.roulette import play_roulette
from games.minesweeper import play_minesweeper
from games.blackjack import play_blackjack
from games.slots import play_slots
from games.craps import play_craps
import os
def dashboard(session):
    while True:
        print("\n================ DASHBOARD ================\n")
        print(" [1] 🎰 Slots              |   [2] 🃏 Blackjack     |   [3] 🎯 Roulette   |   [4] 🎲 Craps ")
        print(" [5] 🥇 Wheel of Fortune   |   [6] 💣 Minesweeper   |   [7] 🪃  Plinko     |   [8] 🚪 Exit")
        print(" [9] ❌ Logout             |  [10] 🪙  Check Balance   ")
        print("\n===========================================\n")
        dash_choice = input("Choose an option: ").strip().lower()
        if dash_choice == "1":
            session, _ = play_slots(session)
        elif dash_choice == "2":
            session = play_blackjack(session)
        elif dash_choice == "3":
            session = play_roulette(session)
        elif dash_choice == "4":
            session = play_craps(session)
        elif dash_choice == "5":
            session = play_wheel_of_fortune(session)
        elif dash_choice == "6":
            session = play_minesweeper(session)
        elif dash_choice == "7":
            session = play_plinko(session)
        elif dash_choice == "8":
            print("🚪 Exiting Termino Casino. Thanks for playing!")
            import sys
            sys.exit(0) 
        elif dash_choice == "9":
           
            SESSION_FILE = os.path.join(os.path.expanduser("~"), ".session.json")
            if os.path.exists(SESSION_FILE):
                try:
                    os.remove(SESSION_FILE)
                    print("🔒 Logged out. Session cleared.")
                except Exception as e:
                    print(f"Error removing session file: {e}")
            return
        elif dash_choice == "10":
            try:
                from airtable0.users import get_user_balance
                username = session.get('username')
                if not username:
                    print("No username found in session.")
                else:
                    coins = get_user_balance(username)
                    print(f"\n🪙  Your current balance: {coins} coins\n")
            except Exception as e:
                print(f"Error fetching balance from Database: {e}")
        else:
            print("Invalid choice. Please try again.")