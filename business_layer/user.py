from db_layer.myutils import Account_manager,ask_category,Expense_manager,update_category,Budget_manager,get_float_input,get_date_input,curr_date_str
import matplotlib.pyplot as plt
from db_layer.database_manager import database_manager
class User:
    def __init__(self,username,password,role):
        self.username=username
        self.password=password
        self.role=role
        self.expense_manager=Expense_manager()
        self.db_manager=database_manager()

    def add_expense1(self):
        try:
            username = self.username
            date = get_date_input('enter date of expense in yyyy--mm--dd:')
            category = ask_category()
            amount = float(input('enter amount of expense:'))
            description = input('enter description of expense:')
            if all([username, date, category, amount]):
                table_name='expenses'
                column=['username','date','category','amount','description']
                values=[username,date,category,amount,description]
                result=self.db_manager.insert_data(table_name,column,values)
                if result:
                    print('Data Inserted successful')
                else:
                    print('Not inserted. Try again')
        except Exception as e:
            print(f'Enter a valid amount,{e}')

    def add_expense(self):
        try:
            username=self.username
            date = get_date_input('enter date of expense in yyyy--mm--dd:')
            category = ask_category()
            amount = float(input('enter amount of expense:'))
            description = input('enter description of expense:')
            if all([username,date,category,amount]):
                result=self.expense_manager.insert_user_expense(username,date,category,amount,description)
                if result:
                    print('inserted sucessful')
                else:
                    print('not inserted')
            else:
                print('All fields are required')
                self.add_expense()

        except Exception as e:
            print(e,'amount should be a number')
            self.add_expense()


    def show_all_expense1(self):
        table_name = 'expenses'
        columns=['expense_id','date','category','amount','description']
        condition=['username=?']
        data=self.db_manager.fetch_data(table_name,columns=columns,where_clause=condition,parameters=[self.username])
        if data:
            print(f"{'expense_id':<15} {'date':<15} {'category':<15} {'amount':<15} {'description':<15}")
            print('-' * 80)
            for e in data:
                expense_id, date , category , amount , description = e
                print(f"{expense_id:<15} {date:<15} {category:<15} {amount:<15} {description:<100}")
            return data
        else:
            print('No data to show')

    def show_all_expense(self):
        data=self.expense_manager.show_all_expense(self.username)
        if data:
            for e in data:
                print(e)
            return data
        else:
            print('No data to show')
        '''-----------------------------'''

    def update_expense1(self):
        print('Following are all your expenses.')
        data = self.show_all_expense1()

        if data:

            try:
                id = int(input('Enter a valid id of an expense to be updated').strip())
            except ValueError:
                print('No valid id is provided.')
                return None

            print("Enter new values for the expense. Press enter to skip a field.")
            filters = {
                'date': input("New date (YYYY-MM-DD): ").strip(),
                'category': update_category().strip(),
                'amount': input("New amount: ").strip(),
                'description': input("New description: ").strip()
            }

            if filters['amount']:
                try:
                    filters['amount'] = float(filters['amount'])
                except ValueError:
                    print("Invalid amount entered. It must be a number.")
                    filters['amount'] = None

            filters = {key: value for key, value in filters.items() if bool(value)}
            condition=['username=?','expense_id=?']
            parameter=[self.username,id]
            result=self.db_manager.update_data(table_name='expenses',
                                               updates=filters,conditions=condition,
                                               parameters=parameter)

            if result:
                print('Updated sucessfull')
            else:
                print('Wrong Expense id is provided. ')


        else:
            print('----------No data to update----------')

    def update_expense(self):
      print('Thses are all expenses.')
      data=self.show_all_expense()
      if data:
        try:
            id=int(input('Enter a valid id of an expense to be updated').strip())
        except ValueError:
            print('No valid id is provided.')
            return None

        print("Enter new values for the expense. Press enter to skip a field.")
        filters = {
            'date': input("New date (YYYY-MM-DD): ").strip(),
            'category': update_category().strip(),
            'amount': input("New amount: ").strip(),
            'description': input("New description: ").strip()
        }

        if filters['amount']:
            try:
                filters['amount'] = float(filters['amount'])
            except ValueError:
                print("Invalid amount entered. It must be a number.")
                filters['amount'] = None

        filters={key:value for key,value in filters.items() if bool(value)}
        filters['expense_id']=id
        self.expense_manager.update_expense(self.username,filters)
      else:
          print('---------No expesne----------')

    def delete_expense1(self):
        print('Thses are all expenses.')
        data = self.show_all_expense1()
        if data:
            try:
                id = int(input('Enter a valid id of an expense to be deleted').strip())
            except ValueError:
                print('No valid id is provided.')
                return None
            table_name='expenses'
            condition=['expense_id=? ','username=?']
            result=self.db_manager.delete_data(table_name=table_name,conditions=condition,parameters=[id,self.username])
            if result:
                print("Deletion sucessfull")
            else:
                print("No record found with given id. Try again")
        else:
            print('----------No expense----------')
    def delete_expense(self):
        print('Thses are all expenses.')
        data=self.show_all_expense()
        if data:
            try:
                id = int(input('Enter a valid id of an expense to be deleted').strip())
            except ValueError:
                print('No valid id is provided.')
                return None
            self.expense_manager.delete_expense(self.username,id)
        else:
            print('----------No expense----------')

    def show_expense_by_category1(self):
        filters = {
            'transport': input('Enter "y" to show transport expenses or Press Enter to skip').strip(),
            'housing': input('Enter "y" to show housing expenses or Press Enter to skip').strip(),
            'food': input('Enter "y" to show food expenses or Press Enter to skip').strip(),
            'clothing': input('Enter "y" to show clothing expenses or Press Enter to skip').strip(),
            'other': input('Enter "y" to show other expenses or Press Enter to skip').strip()
        }
        filters = {key: value for key, value in filters.items() if value == "y"}
        if not filters:
            print('No category is provided.')
        else:
            table_name='expenses'
            columns=['expense_id','date','category','amount','description']
            condition=[' username=? ']
            parameter=[self.username]
            data=self.db_manager.fetch_data(table_name=table_name,columns=columns,where_clause=condition,parameters=parameter)
            if data:
                transport_expense=[]
                housing_expense=[]
                food_expense=[]
                clothing_expense=[]
                other_expense=[]
                category=filters.keys()
                for d in data:
                    if   d[2]=='transport' and ('transport' in category):
                        transport_expense.append(d)
                    elif d[2]=='housing'  and ('housing' in category):
                        housing_expense.append(d)
                    elif d[2]=='food' and  ('food' in category):
                        food_expense.append(d)
                    elif d[2]=='clothing' and  ('clothing' in category):
                        clothing_expense.append(d)
                    elif d[2]=='other' and  ('other' in category):
                        other_expense.append(d)
                expense_data=transport_expense+housing_expense+food_expense+clothing_expense+other_expense
                if expense_data:
                    print(f"{'expense_id':<15} {'date':<15} {'category':<15} {'amount':<15} {'description':<15}")
                    print('-' * 80)
                    for data in expense_data:
                        expense_id, date, category, amount, description = data
                        print(f"{expense_id:<15} {date:<15} {category:<15} {amount:<15} {description:<100}")
                else:
                    print('------No data for specified category------')

            else:
                print('---------No data to show.-----------')
    def show_expense_by_category(self):
        filters={
            'transport':input('Enter "y" to show transport expenses or Press Enter to skip').strip(),
            'housing': input('Enter "y" to show housing expenses or Press Enter to skip').strip(),
            'food': input('Enter "y" to show food expenses or Press Enter to skip').strip(),
            'clothing': input('Enter "y" to show clothing expenses or Press Enter to skip').strip(),
            'other': input('Enter "y" to show other expenses or Press Enter to skip').strip()
        }
        filters={key:value for key,value in filters.items() if value=="y"}
        if not filters:
            print('No category is provided.')
        else:
            self.expense_manager.show_expense_by_category(self.username,filters)

    def show_budget_status_by_category1(self):
        # print('Budget status will be shown on the basis of active budget or latest budget set by you')
        table_name = 'budgets'
        columns = ['housing', 'transport', 'food', 'clothing', 'other', 'start_date', 'end_date']
        condition = ['username=?']
        parameter = [self.username]
        latest_budget = self.db_manager.fetch_data(table_name=table_name, columns=columns, where_clause=condition,
                                                   parameters=parameter)
        # print(latest_budget)
        if latest_budget:
            latest_budget.sort(key=lambda x: x[6],reverse=True)
            latest_budget=latest_budget[0]
            # print(latest_budget)

            start_date=latest_budget[5]
            end_date=latest_budget[6]
            print(f"Your budget start on {start_date} and ends on {end_date}")
            table_name = 'expenses'
            columns = [ 'category', 'amount']
            condition = ['username=?', 'date>=?', 'date<=?']
            parameter = [self.username, start_date, end_date]
            result=self.db_manager.fetch_data(table_name=table_name,
                                              columns=columns,
                                              where_clause=condition,
                                              parameters=parameter)
            # print(result)

            budget_amount = {
                'housing': latest_budget[0],
                'transport': latest_budget[1],
                'food': latest_budget[2],
                'clothing': latest_budget[3],
                'other': latest_budget[4]
            }
            amount_spend = {
                'housing': 0,
                'transport': 0,
                'food': 0,
                'clothing': 0,
                'other': 0
            }

            for e in result:
                category, amount = e
                amount_spend[category] += amount

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


        else:
            print('------NO BUDGET TO SHOW BUDGET STATUS------')
    def show_budget_status_by_category(self):
        print('Budget status will be shown on the basis of active budget or latest budget set by you')
        budget_obj = Budget_manager()
        active_budget = budget_obj.active_budget(self.username)

        if active_budget=='error':
            return
        elif active_budget!='no_active_budget':
            start_date= active_budget[0]
            end_date=active_budget[1]
            print(f'showing expense by category according to budget that start on {start_date} and end on {end_date}')
            budget_amount={
                'housing':active_budget[2],
                'transport':active_budget[3],
                'food':active_budget[4],
                'clothing':active_budget[5],
                'other':active_budget[6]
            }
            amount_spend = {
                'housing': 0,
                'transport': 0,
                'food': 0,
                'clothing': 0,
                'other': 0
            }

            data=self.expense_manager.show_all_expense(self.username)

            for e in data:
                expense_id,date,category,amount,description=e
                if date>=start_date and date<=end_date:
                        amount_spend[category]+=amount

            budget_status={
                'housing': budget_amount['housing']-amount_spend['housing'],
                'transport': budget_amount['transport']-amount_spend['transport'],
                'food': budget_amount['food']-amount_spend['food'],
                'clothing': budget_amount['clothing']-amount_spend['clothing'],
                'other': budget_amount['other']-amount_spend['other']
            }

            print( f'''
            
                           Budget                                     
            housing   -> {budget_amount['housing']}
            transport -> {budget_amount['transport']}
            food      -> {budget_amount['food']}
            clothing  -> {budget_amount['clothing']}
            other     -> {budget_amount['other']}
            
                           spend
                           
            housing   -> {amount_spend['housing']}
            transport -> {amount_spend['transport']}
            food      -> {amount_spend['food']}
            clothing  -> {amount_spend['clothing']}
            other     -> {amount_spend['other']}
            
                         Remaining
                         
            housing   -> {budget_status['housing']}
            transport -> {budget_status['transport']}
            food      -> {budget_status['food']}
            clothing  -> {budget_status['clothing']}
            other     -> {budget_status['other']}

''')

        else:
            prev_budget = budget_obj.prev_budget(self.username)
            # print(prev_budget)
            if prev_budget == 'error':
                return
            elif prev_budget != 'no_prev_budget':
                start_date = prev_budget[0]
                end_date = prev_budget[1]
                print(f'showing expense by category according to budget that start on {start_date} and end on {end_date}')
                budget_amount = {
                    'housing': prev_budget[2],
                    'transport': prev_budget[3],
                    'food': prev_budget[4],
                    'clothing': prev_budget[5],
                    'other': prev_budget[6]
                }
                amount_spend = {
                    'housing': 0,
                    'transport': 0,
                    'food': 0,
                    'clothing': 0,
                    'other': 0
                }
                data = self.expense_manager.show_all_expense(self.username)
                for e in data:
                    expense_id, date, category, amount, description = e
                    if date >= start_date and date <= end_date:
                        amount_spend[category] += amount

                budget_status = {
                    'housing': budget_amount['housing'] - amount_spend['housing'],
                    'transport': budget_amount['transport'] - amount_spend['transport'],
                    'food': budget_amount['food'] - amount_spend['food'],
                    'clothing': budget_amount['clothing'] - amount_spend['clothing'],
                    'other': budget_amount['other'] - amount_spend['other']
                }

                print(f'''

                                           Budget                                     
                                    housing   -> {budget_amount['housing']}
                                    transport -> {budget_amount['transport']}
                                    food      -> {budget_amount['food']}
                                    clothing  -> {budget_amount['clothing']}
                                    other     -> {budget_amount['other']}

                                           spend

                                    housing   -> {amount_spend['housing']}
                                    transport -> {amount_spend['transport']}
                                    food      -> {amount_spend['food']}
                                    clothing  -> {amount_spend['clothing']}
                                    other     -> {amount_spend['other']}

                                         Remaining

                                    housing   -> {budget_status['housing']}
                                    transport -> {budget_status['transport']}
                                    food      -> {budget_status['food']}
                                    clothing  -> {budget_status['clothing']}
                                    other     -> {budget_status['other']}

                ''')
            else:
                print("You don't have any budget set.")



    def plot_expense1(self):
        colors = ['#A4D3EE', '#FFB347', '#BFD8B8', '#F4A460', '#D8BFD8']
        category_expense = {
            'housing': 0,
            'transport': 0,
            'food': 0,
            'clothing': 0,
            'other': 0
        }
        column=['category','amount']
        condition=['username=?']
        data = self.db_manager.fetch_data(table_name='expenses',columns=column,where_clause=condition,parameters=[self.username])
        if data:
            for category, expense in data:
                category_expense[category] += expense

            category_expense={key:value for key,value in category_expense.items() if value}
            labels = [key for key in category_expense.keys()]
            share = [values for values in category_expense.values()]
            color = colors[:len(labels)]
            plt.pie(share, labels=labels, colors=color, startangle=0, shadow=False,
                    explode=(0.1, 0.1, 0.1, 0.1, 0.1)[:len(labels)],
                    radius=1.2, autopct='%1.1f%%')

            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
            plt.show()
            return
        else:
            print('No data to plot')

    def plot_expense(self):
        colors=['#A4D3EE','#FFB347','#BFD8B8','#F4A460','#D8BFD8']
        category_expense={
            'housing':0,
            'transport': 0,
            'food': 0,
            'clothing': 0,
            'other': 0
        }

        # share=[category_expense['housing'],category_expense['transport'],category_expense['food'],category_expense['clothing'],category_expense['other']]
        data=self.expense_manager.plot_expense(self.username)
        if data:#it is returning list of tuple (category,amount)
            for category,expense in data:
                category_expense[category]+=expense
            # print(category_expense)
            category_expense={key:value for key,value in category_expense.items() if value}
            # print(category_expense)


            labels=[key for key in category_expense.keys()]
            share=[values for values in category_expense.values()]
            color=colors[:len(labels)]
            plt.pie(share,labels=labels,colors=color,startangle=0, shadow = False, explode = (0.1, 0.1, 0.1, 0.1,0.1)[:len(labels)],
            radius = 1.2, autopct = '%1.1f%%')

            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
            plt.show()
            return
        else:
            print('No data to plot')

    def set_budget_by_category1(self):
        curr_date=curr_date_str()
        table_name='budgets'
        columns=['housing','transport','food','clothing','other','start_date','end_date']
        condition=['username=?','start_date<=?','end_date>=?']
        parameter=[self.username,curr_date,curr_date]
        active_budget=self.db_manager.fetch_data(table_name=table_name,columns=columns,where_clause=condition,parameters=parameter)
        print(active_budget)
        if active_budget:
            start_date, end_date = active_budget[0][5], active_budget[0][6]
            print(f'you already have an active budget that starts on {start_date} and ends on {end_date}.')

        else:

            prev_budget=self.db_manager.fetch_data(table_name=table_name,
                                                   columns=columns,
                                                   where_clause=['username=?'],
                                                   parameters=[self.username])
            print(prev_budget)
            if prev_budget:
                prev_budget.sort(key=lambda x: x[6],reverse=True)
                prev_budget=prev_budget[0]
                print(prev_budget)
                prev_budget_end_date=prev_budget[6]
                entries = {
                    'username': self.username,
                    'housing': get_float_input('Enter budget for housing category: '),
                    'transport': get_float_input('Enter budget for transport category: '),
                    'food': get_float_input('Enter budget for food category: '),
                    'clothing': get_float_input('Enter budget for clothing category: '),
                    'other': get_float_input('Enter budget for other category: '),
                    'start_date': get_date_input('Enter start date(yyyy-mm--dd) for budget: '),
                    'end_date': get_date_input('Enter end date(yyyy-mm--dd) for budget: ')
                }
                while True:
                    if entries['start_date']>prev_budget_end_date:
                        break
                    else:
                        print(f'start_date should be greater than {prev_budget_end_date} as it is your previous budget end date')
                        entries['start_date']=get_date_input('Enter start date(yyyy-mm--dd) for budget: ')
                while True:
                    if entries['end_date']>=entries['start_date']:
                        break
                    else:
                        print(f'end_date should be greater than or equal to {entries['start_date']}')
                        entries['end_date']=get_date_input('Enter end date(yyyy-mm--dd) for budget: ')
                column=[col for col in entries.keys()]
                value=[val for val in entries.values()]
                result=self.db_manager.insert_data(table_name=table_name,columns=column,values=value)
                if result:
                    print('-------Budget is set.--------')
                else:
                    print('Budget is not set.Try again')
            else:
                print("You don't have any budget.Please set a budget.")
                entries = {
                    'username': self.username,
                    'housing': get_float_input('Enter budget for housing category: '),
                    'transport': get_float_input('Enter budget for transport category: '),
                    'food': get_float_input('Enter budget for food category: '),
                    'clothing': get_float_input('Enter budget for clothing category: '),
                    'other': get_float_input('Enter budget for other category: '),
                    'start_date': get_date_input('Enter start date(yyyy-mm--dd) for budget: '),
                    'end_date': get_date_input('Enter end date(yyyy-mm--dd) for budget: ')
                }
                while True:
                    if entries['end_date'] >= entries['start_date']:
                        break
                    else:
                        print(f'end_date should be greater than or equal to {entries['start_date']}')
                        entries['end_date'] = get_date_input('Enter end date(yyyy-mm--dd) for budget: ')
                column = [col for col in entries.keys()]
                value = [val for val in entries.values()]
                result = self.db_manager.insert_data(table_name=table_name, columns=column, values=value)
                if result:
                    print('-------Budget is set.--------')
                else:
                    print('Budget is not set.Try again')


    def set_budget_by_category(self):
        budget_obj = Budget_manager()
        active_budget=budget_obj.active_budget(self.username)

        if active_budget=='error':
            return
        elif active_budget!='no_active_budget':
            start_date,end_date=active_budget[0],active_budget[1]
            print(f'you alread have an active budget that starts on {start_date} and ends on {end_date}. But you can update it.')
        else:
            prev_budget=budget_obj.prev_budget(self.username)
            if prev_budget=='error':
                return
            elif prev_budget!='no_prev_budget':
                prev_budget_end_date=prev_budget[0][1]
                entries = {
                    'username': self.username,
                    'housing': get_float_input('Enter budget for housing category: '),
                    'transport': get_float_input('Enter budget for transport category: '),
                    'food': get_float_input('Enter budget for food category: '),
                    'clothing': get_float_input('Enter budget for clothing category: '),
                    'other': get_float_input('Enter budget for other category: '),
                    'start_date': get_date_input('Enter start date(yyyy-mm--dd) for budget: '),
                    'end_date': get_date_input('Enter end date(yyyy-mm--dd) for budget: ')
                }
                while True:
                    if entries['start_date']>prev_budget_end_date:
                        break
                    else:
                        print(f'start_date should be greater than {prev_budget_end_date} as it is your previous budget end date')
                        entries['start_date']=get_date_input('Enter start date(yyyy-mm--dd) for budget: ')
                while True:
                    if entries['end_date']>=entries['start_date']:
                        break
                    else:
                        print(f'end_date should be greater than or equal to {entries['start_date']}')
                        entries['end_date']=get_date_input('Enter end date(yyyy-mm--dd) for budget: ')

                budget_obj.insert_user_budget(entries)

            else:
                print("You don't have any budget.Please set a budget.")
                entries = {
                    'username': self.username,
                    'housing': get_float_input('Enter budget for housing category: '),
                    'transport': get_float_input('Enter budget for transport category: '),
                    'food': get_float_input('Enter budget for food category: '),
                    'clothing': get_float_input('Enter budget for clothing category: '),
                    'other': get_float_input('Enter budget for other category: '),
                    'start_date': get_date_input('Enter start date(yyyy-mm--dd) for budget: '),
                    'end_date': get_date_input('Enter end date(yyyy-mm--dd) for budget: ')
                }
                while True:
                    if entries['end_date'] >= entries['start_date']:
                        break
                    else:
                        print(f'end_date should be greater than or equal to {entries['start_date']}')
                        entries['end_date'] = get_date_input('Enter end date(yyyy-mm--dd) for budget: ')

                budget_obj.insert_user_budget(entries)






class Admin(User):
     def show_all_user1(self):
         table_name='users'
         columns=['user_id','username','role']
         result=self.db_manager.fetch_data(table_name=table_name,columns=columns)
         if result:
             for u in result:
                 print(u)
         else:
             print('No user')

     def show_all_user(self):
         user_db=Account_manager()
         result=user_db.show_user()
         if result:
             for u in result:
                 print(u)
         else:
             print('No user')

     def delete_user1(self):
         print('THESE ARE USERS')
         self.show_all_user1()
         user_id = input('ENTER USER_ID TO DELETE A USER')
         try:
             user_id = int(user_id)
         except ValueError:
             print('Id must a valid integer')
             return False
         table_name='users'
         condition=['user_id=? ']
         result=self.db_manager.delete_data(table_name=table_name,conditions=condition,parameters=[user_id])
         if result:
             print('Deletion sucessfull')
         else:
             print('Not deleted. Please provide valid id')

     def delete_user(self):
         print('THESE ARE USERS')
         self.show_all_user()
         user_id=input('ENTER USER_ID TO DELETE A USER')
         try:
            user_id = int(user_id)
         except ValueError:
             print('Id must a valid integer')
             return False
         user_db=Account_manager()
         result=user_db.delete_user(user_id)
         return result

     def show_all_users_expenses1(self):
        table_name = 'expenses'
        columns = ['expense_id','username', 'date', 'category', 'amount', 'description']
        data = self.db_manager.fetch_data(table_name, columns=columns)
        if data:
            for e in data:
                print(e)
            return data
        else:
            print('No data to show')
     def show_all_users_expenses(self):
         self.expense_manager.all_users_expenses()