user_table_name='users'
users_schema = '''(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL UNIQUE,
password TEXT NOT NULL,
role TEXT NOT NULL)
'''


expense_table_name='expenses'
expenses_schema = """
expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
date DATE NOT NULL,
category TEXT NOT NULL,
amount FLOAT NOT NULL,
description TEXT)
"""


budget_table_name='budgets'
budgets_schema = """
budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
housing FLOAT NOT NULL,
transport FLOAT NOT NULL,
food FLOAT NOT NULL,
clothing FLOAT NOT NULL,
other FLOAT NOT NULL,
start_date DATE NOT NULL,
end_date DATE NOT NULL)
"""


def create_table(table_name, schema):
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} {schema}"
        print(create_table_sql)
