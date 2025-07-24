from airtable0 import users

def get_balance(user_id):
    pass

def add_coins(user_id, amount):
    pass

def subtract_coins(user_id, amount):
    pass

def can_bet(user, amount):
    return user['coins'] >= amount and amount > 0

def apply_bet(user, amount, multiplier=0):
    user['coins'] -= amount
    if multiplier > 0:
        user['coins'] += int(amount * multiplier)
    return user