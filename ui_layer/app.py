from business_layer.Auth import Auth
from business_layer.user import User
from db_layer.connection import close_connection
from ui_layer.user_menu import user_menu
from business_layer.Admin import Admin
from ui_layer.admin_menu import admin_menu
logged_in=False
import getpass
def handle_login():
    username = input('enter username:').strip()
    password = input("Enter password").strip()
    if all([username,password]):
        auth_obj=Auth()
        user_data=auth_obj.login1(username,password)
        if user_data:
            print('login successful')
            if user_data[2]=='user':
                user=User(user_data[0],user_data[1],user_data[2])
                user_menu(user,main_menu)
            else:
                user = Admin(user_data[0], user_data[1], user_data[2])
                admin_menu(user,main_menu,user_menu)
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