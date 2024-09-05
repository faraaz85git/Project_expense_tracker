from db_layer.database_manager import database_manager

class Expense:
    def __init__(self):
        self.db_manager=database_manager()

    def add_expense(self,username,date, category, amount, description):
        table_name = 'expenses'
        column = ['username', 'date', 'category', 'amount', 'description']
        values = [username, date, category, amount, description]
        result = self.db_manager.insert_data(table_name, column, values)
        return result

    def get_expense(self,username):
        table_name = 'expenses'
        columns = ['expense_id', 'date', 'category', 'amount', 'description']
        condition = ['username=?']
        data = self.db_manager.fetch_data(table_name,
                                          columns=columns,
                                          where_clause=condition,
                                          parameters=[username])
        return data

    def update_expense(self,username,filters,expense_id):
        if filters['amount']:
            try:
                filters['amount'] = float(filters['amount'])
            except ValueError:
                print("Invalid amount entered. Amount will not be updated.")
                filters['amount'] = None

        filters = {key: value for key, value in filters.items() if bool(value)}
        condition = ['username=?', 'expense_id=?']
        parameter = [username, expense_id]
        result = self.db_manager.update_data(table_name='expenses',
                                             updates=filters, conditions=condition,
                                             parameters=parameter)
        return result

    def delete_expense(self,username,expense_id):
        table_name = 'expenses'
        condition = ['expense_id=? ', 'username=?']
        result = self.db_manager.delete_data(table_name=table_name, conditions=condition,
                                             parameters=[expense_id,username])
        if result:
            print("Deletion sucessfull")
        else:
            print("Try again")