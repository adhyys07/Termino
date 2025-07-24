# Termino Casino

Termino Casino is a terminal-based casino game suite with user authentication, session management, and multiple games. Play, bet, and win coins in a secure, modular Python application!

## Features
- User signup, login, and email verification
- Secure session management (obfuscated session file)
- Dashboard for game selection
- Wheel of Fortune game with multiple multipliers
- Planned games: Slots, Blackjack, Roulette, Craps, Minesweeper, Plinko
- Airtable backend for user and coin management
- Logout and session clearing

## How to Run
1. Clone the repository:
   ```
   git clone https://github.com/adhyys07/Termino.git
   cd Termino
   ```
2. Install Python 3.8+ and required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the app: 
   ```
   python main.py
   ```

## Game List
- Wheel of Fortune (fully implemented)
- Slots (coming soon)
- Blackjack (coming soon)
- Roulette (coming soon)
- Craps (coming soon)
- Minesweeper (coming soon)
- Plinko (coming soon)

## Security
- Session file is obfuscated using base64 and hidden on Windows
- Only verified accounts can log in
- Logout removes credentials and session file

## Contributing
Pull requests and suggestions are welcome!

## License
MIT
