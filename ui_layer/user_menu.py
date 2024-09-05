from db_layer.myutils import get_date_input,ask_category,display,display_budget_status

def user_menu(user,main_menu):
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
'''
        if user.role=='user':
            user_choice+='9.Exit(logout)'
        else:
            user_choice+='9.Back'

        user_input = input(user_choice)
        if user_input == '1':
            try:
                date = get_date_input('enter date of expense in yyyy--mm--dd:')
                category = ask_category()
                amount = float(input('enter amount of expense:'))
                description = input('enter description of expense:')
                result=user.add_expense1(date,category,amount,description)
                if result:
                    print('Data Inserted successful')
                else:
                    print('Not inserted. Try again')
            except ValueError as e:
                print(f'Enter a valid amount,{e}')

        elif user_input == '2':
            data=user.show_all_expense2()
            if data:
                display(data)
            else:
                print('No data to show')

        elif user_input == '3':
            data = user.show_all_expense2()
            if data:
                display(data)
                try:
                    expense_id=int(input('Enter a valid expense id to update expense'))
                    result=user.update_expense2(expense_id)
                    if result:
                        print('Updated successfully.')
                    else:
                        print('Try again.')
                except ValueError as e:
                    print(f'Id must be an integer.')
            else:
                print('No data to show')


        elif user_input == '4':
            data=user.show_all_expense2()
            if data:
                display(data)
                try:
                    expense_id = int(input('Enter a valid id of an expense to be deleted').strip())
                    user.delete_expense2(expense_id)
                except ValueError:
                    print('No valid id is provided.')
            else:
                print('-----------No data to delete.-----------')

        elif user_input == '5':
            filters = {
                'transport': input('Enter "y" to show transport expenses or Press Enter to skip').strip(),
                'housing': input('Enter "y" to show housing expenses or Press Enter to skip').strip(),
                'food': input('Enter "y" to show food expenses or Press Enter to skip').strip(),
                'clothing': input('Enter "y" to show clothing expenses or Press Enter to skip').strip(),
                'other': input('Enter "y" to show other expenses or Press Enter to skip').strip()
            }
            filters = {key: value for key, value in filters.items() if value == "y"}
            user.show_expense_by_category2(filters)

        elif user_input == '6':
            user.set_budget_by_category2()

        elif user_input == '7':
            data=user.show_budget_status_by_category2()
            if data:
                display_budget_status(data[0],data[1])

        elif user_input=='8':
            user.plot_expense1()

        elif user_input == '9':
            break
        else:
            print('wrong input')
    main_menu()