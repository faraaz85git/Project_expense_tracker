from db_layer.myutils import ask_category,update_category,get_float_input,get_date_input,curr_date_str
import matplotlib.pyplot as plt
from db_layer.database_manager import database_manager
from business_layer.Budget import Budget
class User:
    def __init__(self,username,password,role):
        self.username=username
        self.password=password
        self.role=role
        self.db_manager=database_manager()

    def add_expense1(self,date,category,amount,description):
                username = self.username
                table_name='expenses'
                column=['username','date','category','amount','description']
                values=[username,date,category,amount,description]
                result=self.db_manager.insert_data(table_name,column,values)
                return result

    def show_all_expense2(self):
        table_name = 'expenses'
        columns = ['expense_id', 'date', 'category', 'amount', 'description']
        condition = ['username=?']
        data = self.db_manager.fetch_data(table_name,
                                          columns=columns,
                                          where_clause=condition,
                                          parameters=[self.username])
        return data

    def update_expense2(self,expense_id):
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
        condition = ['username=?', 'expense_id=?']
        parameter = [self.username, expense_id]
        result = self.db_manager.update_data(table_name='expenses',
                                             updates=filters, conditions=condition,
                                             parameters=parameter)
        return result

    def delete_expense2(self,expense_id):
        table_name = 'expenses'
        condition = ['expense_id=? ', 'username=?']
        result = self.db_manager.delete_data(table_name=table_name, conditions=condition,
                                             parameters=[expense_id, self.username])
        if result:
            print("Deletion sucessfull")
        else:
            print("Try again")


    def show_expense_by_category2(self,filters):
        if not filters:
            print('No category is provided.')
        else:
            table_name='expenses'
            columns=['expense_id','date','category','amount','description']
            condition=[' username=? ']
            parameter=[self.username]
            data=self.db_manager.fetch_data(table_name=table_name,columns=columns,where_clause=condition,parameters=parameter)
            if data:
                expense_data=[e for e in data if e[2] in filters.keys()]
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

    def show_budget_status_by_category2(self):
        budget=Budget()
        latest_budget=budget.latest_budget(self.username)
        if latest_budget:
            start_date = latest_budget[5]
            end_date = latest_budget[6]
            print(f"Your budget start on {start_date} and ends on {end_date}")
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
            expense_data=self.show_all_expense2()
            for data in expense_data:
                if (data[1]>=start_date and data[1]<=end_date):
                    amount_spend[data[2]]+=data[3]

            budget_status = {
                'housing': budget_amount['housing'] - amount_spend['housing'],
                'transport': budget_amount['transport'] - amount_spend['transport'],
                'food': budget_amount['food'] - amount_spend['food'],
                'clothing': budget_amount['clothing'] - amount_spend['clothing'],
                'other': budget_amount['other'] - amount_spend['other']
            }

            return [budget_amount,amount_spend]

        else:
            print('------NO BUDGET TO SHOW BUDGET STATUS------')

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

    def set_budget_by_category2(self):
        budget=Budget()
        active_budget=budget.active_budget(self.username)
        if active_budget:
            start_date, end_date = active_budget[0][5], active_budget[0][6]
            print(f'you already have an active budget that starts on {start_date} and ends on {end_date}.')
        else:
            prev_budget=budget.latest_budget(self.username)
            if prev_budget:
                prev_budget_end_date = prev_budget[6]
                budget.set_budget(self.username,prev_budget_end_date)

            else:
                print("You don't have any budget.Please set a budget.")
                budget.set_budget(self.username,prev_budget_end_date=None)
