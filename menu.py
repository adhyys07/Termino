from games.wof import play_wheel_of_fortune
from games.plinko import play_plinko
import os
def dashboard(session):
    while True:
        print("\n================ DASHBOARD ================\n")
        print(" [1] 🎰 Slots              |   [2] 🃏 Blackjack     |   [3] 🎯 Roulette   |   [4] 🎲 Craps ")
        print(" [5] 🥇 Wheel of Fortune   |   [6] 💣 Minesweeper   |   [7] 🪃  Plinko     |   [8] 🚪 Exit    | [9] ❌ Logout ")
        print("\n===========================================\n")
        dash_choice = input("Choose an option: ").strip().lower()
        if dash_choice == "1":
            print("Slots game coming soon!")
        elif dash_choice == "2":
            print("Blackjack coming soon!")
        elif dash_choice == "3":
            print("Roulette coming soon!")
        elif dash_choice == "4":
            print("Craps coming soon!")
        elif dash_choice == "5":
            session = play_wheel_of_fortune(session)
        elif dash_choice == "6":
            print("Minesweeper coming soon!")
        elif dash_choice == "7":
            session = play_plinko(session)
        elif dash_choice == "8":
            print("🚪 Exiting Termino Casino. Thanks for playing!")
            import sys
            sys.exit(0)  # Exit program completely
        elif dash_choice == "9":
            # Logout: remove session file if exists
            SESSION_FILE = os.path.join(os.path.expanduser("~"), ".session.json")
            if os.path.exists(SESSION_FILE):
                try:
                    os.remove(SESSION_FILE)
                    print("🔒 Logged out. Session cleared.")
                except Exception as e:
                    print(f"Error removing session file: {e}")
            # Restart login/signup loop
            return
        else:
            print("Invalid choice. Please try again.")