from db_layer.database_manager import database_manager
from custom_exception.custom_exception import SQLiteException
class Expense:
    def __init__(self,logger):
        self.db_manager=database_manager(logger=logger)
        self.logger=logger

    def add_expense(self,username,date, category, amount, description):
        table_name = 'expenses'
        column = ['username', 'date', 'category', 'amount', 'description']
        values = [username, date, category, amount, description]
        try:
            result = self.db_manager.insert_data(table_name, column, values)
            return result
        except Exception:
            raise

    def get_expense(self,username):
        table_name = 'expenses'
        columns = ['expense_id', 'date', 'category', 'amount', 'description']
        condition = ['username=?']
        try:
            data = self.db_manager.fetch_data(table_name,
                                              columns=columns,
                                              where_clause=condition,
                                              parameters=[username])
            return data
        except SQLiteException:
            raise
        except Exception as e:
            self.logger.log(message=str(e),level="error")
            raise

    def update_expense(self,username,filters,expense_id):
        try:
            if filters['amount']:
                try:
                    filters['amount'] = float(filters['amount'])
                except ValueError:
                    self.logger.log(message="Invalid amount.",level="error")
                    raise ValueError("Invalid amount.")
                    # print("Invalid amount entered. Amount will not be updated.")
                    # filters['amount'] = None

            filters = {key: value for key, value in filters.items() if bool(value)}
            condition = ['username=?', 'expense_id=?']
            parameter = [username, expense_id]
            result = self.db_manager.update_data(table_name='expenses',
                                                 updates=filters, conditions=condition,
                                                 parameters=parameter)
            return result
        except Exception as e:
            # print('An error ocurred')
            raise

    def delete_expense(self,username,expense_id):
        try:
            table_name = 'expenses'
            condition = ['expense_id=? ', 'username=?']
            result = self.db_manager.delete_data(table_name=table_name, conditions=condition,
                                                 parameters=[expense_id,username])
            if result:
                self.logger.log(message="Deletion success.")
                print("Deletion sucessfull")
            else:
                self.logger.log(message="Deletion failed.")
                print("Try again")
        except Exception:
            raise