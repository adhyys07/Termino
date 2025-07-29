
# Termino Casino

Termino Casino is a terminal-based casino game suite with user authentication, session management, and a variety of classic games. Play, bet, and win coins in a secure, modular Python application backed by Airtable.

---

## Features

- **User Authentication**: Signup, login, and email verification with secure password hashing.
- **Session Management**: Obfuscated session file, auto-login, and secure logout.
- **Dashboard**: Easy game selection and account management.
- **Games**: Wheel of Fortune, Slots, Blackjack, Roulette, Craps, Minesweeper, Plinko (all fully implemented).
- **Airtable Backend**: Persistent user, coin, and play history management.
- **Admin Play Logs**: All game activity is logged for admin review.
- **Security**: Environment variables for all secrets, session file hidden on Windows, only verified accounts can log in.

---

## Setup & Installation

### 1. Clone the repository
```sh
git clone https://github.com/adhyys07/Termino.git
cd Termino
```

### 2. Install Python and dependencies
- Python 3.8 or higher is required.
- Install dependencies:
```sh 
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```
SMTP_PASSWORD=your_smtp_app_password
AIRTABLE_API_KEY=your_airtable_api_key
```

### 4. Run the Application
```sh
python main.py
```

---

## Game List & Rules

- **Wheel of Fortune**: Spin for multipliers, jackpots, or bankruptcies.
- **Slots**: Classic slot machine with random payouts.
- **Blackjack**: Beat the dealer to 21, with full hit/stand logic.
- **Roulette**: Bet on numbers, colors, or ranges. Multiple bet types coming soon.
- **Craps**: Roll the dice, win on natural, lose on craps, or play the point.
- **Minesweeper**: Bet and reveal safe cells for increasing profit, cash out before hitting a mine.
- **Plinko**: Drop a ball, win based on where it lands.

---

## Security & Best Practices

- **Environment Variables**: All sensitive keys (SMTP, Airtable) are loaded from `.env` and never committed.
- **.env in .gitignore**: Ensure `.env` is listed in `.gitignore` to keep secrets safe.
- **Session File**: Obfuscated and hidden on Windows, only stores minimal info for auto-login.
- **Email Verification**: Only verified users can log in and play.
- **Play Logging**: All game activity is logged to Airtable for admin review.

---

## Project Structure

- `main.py` — Entry point, session and email logic
- `auth.py` — Signup, login, and verification
- `menu.py` — Dashboard and game selection
- `games/` — All game modules (wof.py, slots.py, blackjack.py, etc.)
- `airtable0/` — Airtable API logic and config
- `core/` — Economy and utility functions

---

## Contributing

Pull requests, bug reports, and suggestions are welcome! Please open an issue or PR on GitHub.

---

