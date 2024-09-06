
myfun=lambda : 1


def admin_menu(user,main_menu,user_menu):
    while True:
        option='''
Enter your choice:
1.User functions
2.Admin functions
3.Exit(logout)
'''
        choice=input(option)
        if   choice=='1':
              user_menu(user,myfun)
        elif choice=='2':
              while True:
                  admin_function=f'''
--------------------------------------------------------
               Welcome {user.username}
--------------------------------------------------------    
enter your choice:
1.Show all users
2.Show all users expenses
3.Delete user
4.Back
'''
                  user_input=input(admin_function)
                  if user_input=='1':
                      user.show_all_user1()
                  elif user_input=='2':
                      user.show_all_users_expenses1()
                  elif user_input=='3':
                      user.delete_user1()
                  elif user_input=="4":
                      break
                  else:
                      print('Wrong input.')
        elif choice=='3':
            break
    main_menu()