from airtable0 import users

def get_balance(user_id):
    # Fetch user info and return coin balance
    # This assumes you have a function to get user by id (implement if needed)
    pass

def add_coins(user_id, amount):
    # Add coins to user balance
    # Fetch user, update coins, and save
    pass

def subtract_coins(user_id, amount):
    # Subtract coins from user balance
    # Fetch user, update coins, and save
    pass

def can_bet(user, amount):
    return user['coins'] >= amount and amount > 0

def apply_bet(user, amount, multiplier=0):
    if multiplier > 0:
        user['coins'] += amount * multiplier
    else:
        user['coins'] -= amount
    return user