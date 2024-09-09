from db_layer.database_manager import database_manager
from db_layer.myutils import curr_date_str,get_float_input,get_date_input
class Budget:
    def __init__(self):
        self.db_manager=database_manager()

    def active_budget(self,username):
        curr_date = curr_date_str()
        table_name = 'budgets'
        columns = ['housing', 'transport', 'food', 'clothing', 'other', 'start_date', 'end_date']
        condition = ['username=?', 'start_date<=?', 'end_date>=?']
        parameter = [username, curr_date, curr_date]
        active_budget = self.db_manager.fetch_data(table_name=table_name, columns=columns, where_clause=condition,
                                                   parameters=parameter)

        return active_budget

    def latest_budget(self,username):
        table_name = 'budgets'
        columns = ['housing', 'transport', 'food', 'clothing', 'other', 'start_date', 'end_date']
        prev_budget = self.db_manager.fetch_data(table_name=table_name,
                                                 columns=columns,
                                                 where_clause=['username=?'],
                                                 parameters=[username])
        # print(prev_budget)
        if prev_budget:
            prev_budget.sort(key=lambda x: x[6], reverse=True)
            prev_budget = prev_budget[0]
            # print(prev_budget)
            return prev_budget
        else:
            return None


    def set_budget(self,username,prev_budget_end_date):
        entries = {
            'username': username,
            'housing': get_float_input('Enter budget for housing category: '),
            'transport': get_float_input('Enter budget for transport category: '),
            'food': get_float_input('Enter budget for food category: '),
            'clothing': get_float_input('Enter budget for clothing category: '),
            'other': get_float_input('Enter budget for other category: '),
            'start_date': get_date_input('Enter start date(yyyy-mm--dd) for budget: '),
            'end_date': get_date_input('Enter end date(yyyy-mm--dd) for budget: ')
        }

        if prev_budget_end_date:
            while True:
                if entries['start_date'] > prev_budget_end_date:
                    break
                else:
                    print(f'start_date should be greater than {prev_budget_end_date} as it is your previous budget end date')
                    entries['start_date'] = get_date_input('Enter start date(yyyy-mm--dd) for budget: ')
            while True:
                if entries['end_date'] >= entries['start_date']:
                    break
                else:
                    print(f'end_date should be greater than or equal to {entries['start_date']}')
                    entries['end_date'] = get_date_input('Enter end date(yyyy-mm--dd) for budget: ')

        else:
                while True:
                    if entries['end_date'] >= entries['start_date']:
                        break
                    else:
                        print(f'end_date should be greater than or equal to {entries['start_date']}')
                        entries['end_date'] = get_date_input('Enter end date(yyyy-mm--dd) for budget: ')
        column = [col for col in entries.keys()]
        value = [val for val in entries.values()]
        table_name = 'budgets'
        result = self.db_manager.insert_data(table_name=table_name, columns=column, values=value)
        if result:
             print('-------Budget is set.--------')
        else:
             print('Budget is not set.Try again')
