import sqlite3
from datetime import datetime
from db_layer.connection import get_connection
import bcrypt
import re
'''-------------------------utility functions----------------------------------'''

def get_float_input(prompt):
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Invalid input.")
            return get_float_input(prompt)
        except Exception as e:
            print(f"An error occurred: {e}.")
            return get_float_input(prompt)

def get_date_input(prompt):
    user_input = input(prompt).strip()

    if not user_input:
        date=datetime.now()
        return date.strftime('%Y-%m-%d')

    try:
        date_obj = datetime.strptime(user_input, '%Y-%m-%d')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        print("Please enter a valid the date in yyyy-mm-dd format.")
        return get_date_input(prompt)


def ask_category():
        choice=input('''
enter category of expense:
1.housing
2.transport
3.food
4.clothing
5.other''')
        if choice=='1':
            return 'housing'
        elif choice=='2':
            return 'transport'
        elif choice=='3':
            return 'food'
        elif choice=='4':
            return 'clothing'
        elif choice=='5':
            return 'other'
        else:
            print('wrong input')
            ask_category()

def update_category():
    choice = input('''
enter new category of expense or press enter to skip:
1.housing
2.transport
3.food
4.clothing
5.other''')
    if choice == '1':
        return 'housing'
    elif choice == '2':
        return 'transport'
    elif choice == '3':
        return 'food'
    elif choice == '4':
        return 'clothing'
    elif choice == '5':
        return 'other'
    else:
        return ''

def curr_date_str():
    date_obj=datetime.now()
    date_str=date_obj.strftime('%Y-%m-%d')
    return date_str

def get_int_input(promt='enter an integer value.'):
    user_input=input(promt)
    try:
        user_input=int(user_input)
        return user_input
    except ValueError:
        print('Enter a valid intger.')
        get_int_input(promt)

def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password

def verify_password(stored_hash, password):
    # Verify that the provided password matches the stored hash
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

def display(expense_data):
    print(f"{'expense_id':<15} {'date':<15} {'category':<15} {'amount':<15} {'description':<15}")
    print('-' * 80)
    for data in expense_data:
        expense_id, date, category, amount, description = data
        print(f"{expense_id:<15} {date:<15} {category:<15} {amount:<15} {description:<100}")

def display_budget_status(budget_amount,amount_spend):
    budget_status = {
        'housing': budget_amount['housing'] - amount_spend['housing'],
        'transport': budget_amount['transport'] - amount_spend['transport'],
        'food': budget_amount['food'] - amount_spend['food'],
        'clothing': budget_amount['clothing'] - amount_spend['clothing'],
        'other': budget_amount['other'] - amount_spend['other']
    }
    print(f'{'Category':<9} {'Budget':>15} {'Spend':>15} {'Remaining':>15}')
    print('-' * 60)
    print(f'{'Housing':<9} {budget_amount['housing']:>15} {amount_spend['housing']:>15} {budget_status['housing']:>15}')
    print(f'{'Transport':<9} {budget_amount['transport']:>15} {amount_spend['transport']:>15} {budget_status['transport']:>15}')
    print(f'{'Food':<9} {budget_amount['food']:>15} {amount_spend['food']:>15} {budget_status['food']:>15}')
    print(f'{'Clothing':<9} {budget_amount['clothing']:>15} {amount_spend['clothing']:>15} {budget_status['clothing']:>15}')
    print(f'{'Other':<9} {budget_amount['other']:>15} {amount_spend['other']:>15} {budget_status['other']:>15}')


def validate_username(username):
    pattern = r'^(?=.*[a-z])(?=.*[0-9])[a-z0-9]+$'
    if re.match(pattern, username):
        return True
    else:
        return False


def validate_password(password):
    pattern = r'^[0-9]{8,}$'

    if re.match(pattern, password):
        return True
    else:
        return False
