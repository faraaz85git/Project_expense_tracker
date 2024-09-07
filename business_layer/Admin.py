from business_layer.user import User


class Admin(User):
    def show_all_user1(self):
        table_name = 'users'
        columns = ['user_id', 'username', 'role']
        result = self.db_manager.fetch_data(table_name=table_name, columns=columns)
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
        table_name = 'users'
        condition = ['user_id=? ']
        result = self.db_manager.delete_data(table_name=table_name, conditions=condition, parameters=[user_id])
        if result:
            print('Deletion sucessfull')
        else:
            print('Not deleted. Please provide valid id')

    # def delete_user(self):
    #     print('THESE ARE USERS')
    #     self.show_all_user()
    #     user_id = input('ENTER USER_ID TO DELETE A USER')
    #     try:
    #         user_id = int(user_id)
    #     except ValueError:
    #         print('Id must a valid integer')
    #         return False
    #     user_db = Account_manager()
    #     result = user_db.delete_user(user_id)
    #     return result

    def show_all_users_expenses1(self):
        table_name = 'expenses'
        columns = ['expense_id', 'username', 'date', 'category', 'amount', 'description']
        data = self.db_manager.fetch_data(table_name, columns=columns)
        if data:
            print(f"{'expense_id':<15} {'username':<15} {'date':<15} {'category':<15} {'amount':<15} {'description':<15}")
            print('-' * 90)
            for e in data:
                expense_id, username, date, category, amount, description = e
                print(f"{expense_id:<15} {username:<15} {date:<15} {category:<15} {amount:<15} {description:<100}")
            return data
        else:
            print('No data to show')
cd Pyc  