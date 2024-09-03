from business_layer.Auth import Auth
from business_layer.user import User,Admin
from db_layer.connection import close_connection

logged_in=False

def user_menu(user):
    while True:
        user_choice = f'''
--------------------------------------------------------
              Welcome {user.username}.
--------------------------------------------------------
enter your choice:
1.Add my expense
2.Show all my expenses
3.Update my expense
4.Delete my expense
5.Show my expense by category
6.set budget category-wise
7.Show budget status by category
8.Plot my expense
9.for quit(logout)
'''
        user_input = input(user_choice)
        if user_input == '1':
            user.add_expense1()

        elif user_input == '2':
            user.show_all_expense1()

        elif user_input == '3':
            user.update_expense1()

        elif user_input == '4':
            user.delete_expense1()

        elif user_input == '5':
            user.show_expense_by_category1()

        elif user_input == '6':
            user.set_budget_by_category1()

        elif user_input == '7':
            user.show_budget_status_by_category1()

        elif user_input=='8':
            user.plot_expense1()

        elif user_input == '9':
            break
        else:
            print('wrong input')
    main_menu()

def admin_menu(user):
    while True:
        user_choice = f'''
--------------------------------------------------------
               Welcome {user.username}
--------------------------------------------------------
enter your choice:
1.Add my expense
2.Show all my expense
3.Update my expense
4.Delete my expense
5.Show my expense by category
6.set budget categorywise
8.Plot your expense
9.show all user
10.show all user expense
11.Delete user
12.for quit(logout)
'''
        user_input = input(user_choice)
        if user_input == '1':
            user.add_expense1()

        elif user_input == '2':
            data=user.show_all_expense1()
            if not data:
                print('No expense')

        elif user_input == '3':
            user.update_expense1()

        elif user_input == '4':
            user.delete_expense1()

        elif user_input == '5':
            user.show_expense_by_category1()

        elif user_input == '6':
            user.set_budget_by_category1()

        elif user_input == '7':
            user.show_budget_status_by_category1()

        elif user_input == '8':
            user.plot_expense1()

        elif user_input == '9':
            user.show_all_user1()

        elif user_input=='10':
            user.show_all_users_expenses1()

        elif user_input == '11':
            user.delete_user1()


        elif user_input == '12':
            break
        else:
            print('wrong input')
    main_menu()

def handle_login():
    username = input('enter username:').strip()
    password = input('enter password:').strip()
    if all([username,password]):
        auth_obj=Auth()
        user_data=auth_obj.login1(username,password)
        if user_data:
            print('login sucessful')
            if user_data[2]=='user':
                user=User(user_data[0],user_data[1],user_data[2])
                user_menu(user)
            else:
                user = Admin(user_data[0], user_data[1], user_data[2])
                admin_menu(user)
        else:
            print('Invlaid username and password')
            main_menu()
    else:
        print('All fields are required')
        main_menu()

def handle_signup():
    username=input('enter username:').strip()
    password=input('enter passwprd:').strip()
    role=input('enter 1.user 2.admin').strip()
    if role=='1':
        role='user'
    elif role=='2':
        role='admin'
    else:
        role='user'

    if all([username,password,role]):
        auth_obj = Auth()
        result=auth_obj.sign_up1(username,password,role)
        if result:
            print('sign up sucessful')
            main_menu()
        else:
            print('username exists')
            main_menu()
    else:
        print('All field are required')
        main_menu()

def main_menu():
    menu='''
----------------------------------
Hellow, Welcome to Expense tracker
----------------------------------
Enter your choice:
1.login
2.signup
3.Exit
----------------------------------'''
    print(menu)
    user_choice=input('Your choice: ')
    if user_choice=='1':
        handle_login()

    elif user_choice=='2':
        handle_signup()

    elif user_choice=='3':
        close_connection()
        exit()
    else:
        print('Wrong input please enter again')
        main_menu()


if __name__=='__main__':
    main_menu()






"""version 1
from Auth import Auth
from user import User,Admin
from connection import close_connection
logged_in=False

def welcome():
    print('''
----------------------------------
Hellow, Welcome to Expense tracker
----------------------------------''')
    user_choice = '''
Enter your choice:
1.login
2.signup
3.Exit
'''
    print(user_choice)

def user_menu(user):
    while True:
        user_choice = f'''Welcome {user.username}.You are singed in as {user.role}
               enter your choice:
               1.Add my expense
               2.Show all my expenses
               3.Update my expense
               4.Delete my expense
               5.Show my expense by category
               6.set budget categorywise
               7.Show budget status by category
               8.Plot my expense
               9.for quit(logout)
               '''
        user_input = input(user_choice)
        if user_input == '1':
            user.add_expense()

        elif user_input == '2':
            user.show_all_expense()

        elif user_input == '3':
            user.update_expense()

        elif user_input == '4':
            user.delete_expense()

        elif user_input == '5':
            user.show_expense_by_category()

        elif user_input == '6':
            user.set_budget_by_category()

        elif user_input == '7':
            user.show_budget_status_by_category()

        elif user_input=='8':
            user.plot_expense()

        elif user_input == '9':
            break
        else:
            print('wrong input')
    menu()

def admin_menu(user):
    while True:
        user_choice = f'''Welcome {user.username}.You are singed in as {user.role}
               enter your choice:
               1.Add my expense
               2.Show all my expense
               3.Update my expense
               4.Delete my expense
               5.Show my expense by category
               6.set budget categorywise
               7.Show budget status by category
               8.Plot your expense
               9.show all user
               10.show all user expense
               11.Delete user
               12.for quit(logout)
               '''
        user_input = input(user_choice)
        if user_input == '1':
            user.add_expense()

        elif user_input == '2':
            data=user.show_all_expense()
            if not data:
                print('No expense')

        elif user_input == '3':
            user.update_expense()

        elif user_input == '4':
            user.delete_expense()

        elif user_input == '5':
            user.show_expense_by_category()

        elif user_input == '6':
            user.set_budget_by_category()

        elif user_input == '7':
            user.show_budget_status_by_category()

        elif user_input == '8':
            user.plot_expense()

        elif user_input == '9':
            user.show_all_user()

        elif user_input=='10':
            user.show_all_users_expenses()

        elif user_input == '11':
            if user.delete_user():
                print('user deleted')
            else:
                print('user not found')

        elif user_input == '12':
            break
        else:
            print('wrong input')
    menu()

def login_option():
    username = input('enter username:').strip()
    password = input('enter password:').strip()
    if all([username,password]):
        auth_obj=Auth()
        user_data=auth_obj.login(username,password)
        if user_data:
            print('login sucessful')
            if user_data[2]=='user':
                user=User(user_data[0],user_data[1],user_data[2])
                user_menu(user)
            else:
                user = Admin(user_data[0], user_data[1], user_data[2])
                admin_menu(user)
        else:
            print('Invlaid username and password')
            menu()
    else:
        print('All fields are required')
        menu()

def signup():
    username=input('enter username:').strip()
    password=input('enter passwprd:').strip()
    role=input('enter 1.user 2.admin').strip()
    if role=='1':
        role='user'
    elif role=='2':
        role='admin'
    else:
        role='user'

    if all([username,password,role]):
        auth_obj = Auth()
        result=auth_obj.sign_up(username,password,role)
        if result:
            print('sign up sucessful')
            menu()
        else:
            print('username exists')
            menu()
    else:
        print('All field are required')
        menu()



def start2(user):
    pass
# def start1():
#     user_choice = '''Enter your choice:
#     1.login
#     2.signup
#     3.'q' for exit
#     '''
#     user_input=input(user_choice)
#     while user_input!='q':
#
#         if user_input=='1':
#             while True:
#                 username = input('Enter username:').strip()
#                 password = input('Enter password:').strip()
#                 role_choice=input('enter 1.user  2.admin').strip()
#
#                 if all([username,password,role]):
#                     if login_option(username,password)==True:
#                         user=User(username,password)
#                         start2(user)
#
#         elif user_input=='2':
#             signup()
#         else:
#             print('wrong input')
#         user_input=input(user_choice)
def menu():
    welcome()
    user_choice=input('Enter your choice')
    if user_choice=='1':
        login_option()

    elif user_choice=='2':
        signup()

    elif user_choice=='3':
        close_connection()
        exit()
    else:
        print('Wrong input please enter again')
        menu()

menu()
"""
'''--------------------------------------------------------'''
#version2
# user_functions='''1.Add my expense
# 2.Show all my expenses
# 3.Update my expense
# 4.Delete my expense
# 5.Show my expense by category
# 6.set budget category-wise
# 7.Show budget status by category
# 8.Plot my expense
# 9.for quit(logout)
# '''
#
# admin_functions='''
# 1.Add my expense
# 2.Show all my expense
# 3.Update my expense
# 4.Delete my expense
# 5.Show my expense by category
# 6.set budget category-wise
# 7.Show budget status by category
# 8.Plot your expense
# 9.show all user
# 10.show all user expense
# 11.Delete user
# 12.for quit(logout)
# '''
#
# def user_menu1(user):
#     print(f'''
# -----------Welcome {user.username}. You are singed in as {user.role}-----------
# ''')
#     while True:
#         print()
#         print('Select from following')
#         print(user_functions)
#         user_input=input("Enter your choice: ")
#         if user_input == '1':
#             user.add_expense()
#
#         elif user_input == '2':
#             user.show_all_expense()
#
#         elif user_input == '3':
#             user.update_expense()
#
#         elif user_input == '4':
#             user.delete_expense()
#
#         elif user_input == '5':
#             user.show_expense_by_category()
#
#         elif user_input == '6':
#             user.set_budget_by_category()
#
#         elif user_input == '7':
#             user.show_budget_status_by_category()
#
#         elif user_input=='8':
#             user.plot_expense()
#
#         elif user_input == '9':
#             break
#         else:
#             print('wrong input')
#     main_menu()
#
# def admin_menu1(user):
#     print(f'''Welcome {user.username}. You are singed in as {user.role}''')
#     while True:
#         print('Select from following')
#         print(user_functions)
#         user_input = input("Enter your choice: ")
#         if user_input == '1':
#             user.add_expense()
#
#         elif user_input == '2':
#             data = user.show_all_expense()
#             if not data:
#                 print('No expense')
#
#         elif user_input == '3':
#             user.update_expense()
#
#         elif user_input == '4':
#             user.delete_expense()
#
#         elif user_input == '5':
#             user.show_expense_by_category()
#
#         elif user_input == '6':
#             user.set_budget_by_category()
#
#         elif user_input == '7':
#             user.show_budget_status_by_category()
#
#         elif user_input == '8':
#             user.plot_expense()
#
#         elif user_input == '9':
#             user.show_all_user()
#
#         elif user_input == '10':
#             user.show_all_users_expenses()
#
#         elif user_input == '11':
#             if user.delete_user():
#                 print('user deleted')
#             else:
#                 print('user not found')
#
#         elif user_input == '12':
#             break
#         else:
#             print('wrong input')
# def handle_login():
#     username = input('enter username:').strip()
#     password = input('enter password:').strip()
#     if all([username, password]):
#         auth_obj = Auth()
#         user_data = auth_obj.login(username, password)
#         if user_data:
#             print('login sucessful')
#             if user_data[2] == 'user':
#                 user = User(user_data[0], user_data[1], user_data[2])
#                 user_menu1(user)
#             else:
#                 user = Admin(user_data[0], user_data[1], user_data[2])
#                 admin_menu1(user)
#         else:
#             print('Invlaid username and password')
#             main_menu()
#     else:
#         print('All fields are required')
#         main_menu()
# def handle_signup():
#     username = input('enter username:').strip()
#     password = input('enter passwprd:').strip()
#     role = input('enter 1.user 2.admin').strip()
#     if role == '1':
#         role = 'user'
#     elif role == '2':
#         role = 'admin'
#     else:
#         role = 'user'
#
#     if all([username, password, role]):
#         auth_obj = Auth()
#         result = auth_obj.sign_up(username, password, role)
#         if result:
#             print('sign up sucessful')
#             main_menu()
#         else:
#             print('username exists')
#             main_menu()
#     else:
#         print('All field are required')
#         main_menu()
# def print_menu():
#     print('''
# ----------------------------------
# Hellow, Welcome to Expense tracker
# ----------------------------------''')
#     user_choice = '''
# Enter your choice:
# 1.login
# 2.signup
# 3.Exit
# '''
#     print(user_choice)
# def main_menu():
#     print_menu()
#     user_choice=input('Enter your choice: ')
#     if user_choice=='1':
#         handle_login()
#
#     elif user_choice=='2':
#         handle_signup()
#
#     elif user_choice=='3':
#         close_connection()
#         exit()
#     else:
#         print('Wrong input please enter again')
#         main_menu()
#
# main_menu()
#
"""--------------------------------------------------------"""
