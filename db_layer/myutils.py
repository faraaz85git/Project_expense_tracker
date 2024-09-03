import sqlite3
from datetime import datetime
from db_layer.connection import get_connection
import bcrypt
class Account_manager:
    def __init__(self):
        self.connection=get_connection()
    def create_user_table(self):
        cursor=self.connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL UNIQUE,password TEXT NOT NULL,role TEXT NOT NULL)')
        self.connection.commit()
    def login(self,username,password):
        cursor=self.connection.cursor()
        query_find_user='SELECT username,password,role FROM users WHERE username=?'
        cursor.execute(query_find_user,(username,))
        user_data=cursor.fetchone()
        self.connection.commit()
        return user_data

    def sign_up(self,username,password,role):
        cursor=self.connection.cursor()
        query='SELECT * FROM users WHERE username=?'
        cursor.execute(query,(username,))
        data=cursor.fetchone()
        if data:
            return False
        else:
            insert_query='INSERT INTO users(username,password,role) VALUES(?,?,?)'
            cursor.execute(insert_query,(username,password,role))
            self.connection.commit()

            return True
    def show_user(self):
        cursor=self.connection.cursor()
        query='SELECT user_id,username,role FROM users'
        cursor.execute(query)
        result=cursor.fetchall()
        return result

    def delete_user(self,user_id):
        cursor=self.connection.cursor()
        query_find_user='SELECT * FROM users WHERE user_id=?'
        cursor.execute(query_find_user,(user_id,))
        if cursor.fetchone():
            delete_query='DELETE FROM users WHERE user_id=?'
            cursor.execute(delete_query,(user_id,))
            self.connection.commit()
            return True
        else:
            return False
    # def close(self):
    #     self.connection.close()


class Expense_manager:
    def __init__(self):
        self.connection=get_connection()

    def create_expense_table(self):
        cursor=self.connection.cursor()
        query='''CREATE TABLE IF NOT EXISTS expenses(
        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        date DATE NOT NULL,
        category TEXT NOT NULL,
        amount FLOAT NOT NULL,
        description TEXT)'''
        cursor.execute(query)
        self.connection.commit()

    def insert_user_expense(self,username,date,category,amount,description=None):
        cursor=self.connection.cursor()
        query='INSERT INTO expenses(username,date,category,amount,description) VALUES(?,?,?,?,?)'
        cursor.execute(query,(username,date,category,amount,description))
        self.connection.commit()
        return True


    def show_all_expense(self,username):
        self.create_expense_table()
        cursor = self.connection.cursor()
        query=('SELECT expense_id,'
               'date,category,amount,'
               'description '
               'FROM expenses WHERE username=?')
        cursor.execute(query, (username,))
        data=cursor.fetchall()
        # for e in data:
        #     print(e)
        return data

    def update_expense(self,username,filters):
        query = "UPDATE expenses SET "
        params = []
        columns = []

        if 'date' in filters:
            columns.append("date = ?")
            params.append(filters['date'])
        if 'category' in filters:
            columns.append("category = ?")
            params.append(filters['category'])
        if 'amount' in filters:
            columns.append("amount = ?")
            params.append(filters['amount'])
        if 'description' in filters:
            columns.append("description = ?")
            params.append(filters['description'])


        if not columns:
            print("No fields provided for update.")
            return


        query += ", ".join(columns)


        query += " WHERE username = ? AND expense_id = ?"
        params.append(username)
        params.append(filters['expense_id'])

        params=tuple(params)
        # print(params)
        try:
            cursor=self.connection.cursor()
            cursor.execute(query, params)


            self.connection.commit()


            if cursor.rowcount == 0:
                print("No record found with the provided ID.")
            else:
                print("Record updated successfully.")

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

    def delete_expense(self,username, exp_id):
        try:
            cursor=self.connection.cursor()
            query='DELETE FROM expenses WHERE username=? AND expense_id=?'
            cursor.execute(query,(username,exp_id))
            self.connection.commit()
            if cursor.rowcount==0:
                print('No record found with given id')

            else:
                print('Record deleted')
        except Exception as e:
            print(f'SQLite error: {e}')

    def show_expense_by_category(self,username,filters):
        query='SELECT expense_id,date,category,amount,description FROM expenses WHERE username=? AND ('
        columns=[]
        params=[username]
        if filters.get('clothing'):
            columns.append('category=?')
            params.append('clothing')

        if filters.get('transport'):
            columns.append('category=?')
            params.append('transport')

        if filters.get('food'):
            columns.append('category=?')
            params.append('food')

        if filters.get('housing'):
            columns.append('category=?')
            params.append('housing')

        if filters.get('other'):
            columns.append('category=?')
            params.append('other')

        query+=(' OR ').join(columns)
        query+=')'
        # print(query)
        params=tuple(params)
        # print(params)
        try:
            cursor=self.connection.cursor()
            cursor.execute(query,params)
            data=cursor.fetchall()
            if not data:
                print('No record found.')
            else:
                for e in data:
                    print(e)

        except Exception as e:
            print(f'SQLite error: {e}')

    def show_budget_status_by_category(self):
        pass

    def plot_expense(self,username):
        query='''
        SELECT category,amount FROM expenses
         WHERE username=?'''
        try:
            cursor=self.connection.cursor()
            cursor.execute(query,(username,))
            data=cursor.fetchall()
            return data
        except Exception as e:
            print(f'SQLite error: {e}')
            return None

    def set_budget_by_category(self):
        pass

    def all_users_expenses(self):
        self.create_expense_table()
        cursor = self.connection.cursor()
        query = 'SELECT expense_id,username,date,category,amount,description FROM expenses'
        cursor.execute(query)
        data = cursor.fetchall()
        for e in data:
            print(e)


class Budget_manager:
    def __init__(self):
        self.connection=get_connection()


    def create_budget_table(self):
        try:
            cursor=self.connection.cursor()
            query='''CREATE TABLE IF NOT EXISTS budgets(
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT NOT NULL,
            housing   FLOAT NOT NULL,
            transport FLOAT NOT NULL,
            food      FLOAT NOT NULL,
            clothing  FLOAT NOT NULL,
            other     FLOAT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL
            )'''
            cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            print(f'SQLite error, {e}')

    def insert_user_budget(self,entries):
        self.create_budget_table()
        query='''
        INSERT INTO budgets(username,housing,transport,food,
        clothing,other,start_date,end_date) VALUES(?,?,?,?,?,?,?,?)'''
        params=[v for v in entries.values()]

        try:
            cursor=self.connection.cursor()
            cursor.execute(query,params)
            self.connection.commit()
            if cursor.rowcount==0:
                print('Record not inserted')
            else:
                print('Record inserted')
        except Exception as e:
            print(f'SQLite exception,{e}')

    def active_budget(self,username):
        self.create_budget_table()
        today_date=curr_date_str()
        query='''
        SELECT start_date,end_date,housing,transport,food,clothing,other FROM budgets 
        where username=? AND (start_date<=? AND end_date>=?)'''
        try:
            cursor=self.connection.cursor()
            cursor.execute(query,(username,today_date,today_date))
            result=cursor.fetchone()
            if result:
                return result
            else:
                return 'no_active_budget'
        except Exception as e:
            print(f'SQLite exception,{e}')
            return 'error'
    def prev_budget(self,username):
        query='''
        SELECT start_date,end_date,housing,transport,food,clothing,other FROM budgets 
        where username=? ORDER BY end_date DESC LIMIT 1'''
        try:
            cursor=self.connection.cursor()
            cursor.execute(query,(username,))
            result=cursor.fetchone()
            if result:
                return result
            else:
                return 'no_prev_budget'
        except Exception as e:
            print(f'SQLite exception,{e}')
            return 'error'





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

'''-------------------------utility functions----------------------------------'''
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

